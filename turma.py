import os, json, subprocess, atexit, copy, datetime

# Exportando funções de acesso
__all__ = ["get_turma", "get_turmas", "set_max_alunos", "add_turma", "del_turma", "is_final", 
           "is_ativa", "abre_turma"]

# Globais
_SCRIPT_DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))
_DATA_DIR_PATH: str = os.path.join(_SCRIPT_DIR_PATH, "data")
_COMPACTADOR_PATH: str = os.path.join(_SCRIPT_DIR_PATH, "compactador.exe")
_ID_FILE_PATH: str = os.path.join(_DATA_DIR_PATH, "proximo_id.txt")
_TURMAS_JSON_FILE_PATH: str = os.path.join(_DATA_DIR_PATH, "turmas.json")
_TURMAS_BIN_FILE_PATH: str = _TURMAS_JSON_FILE_PATH.replace(".json", ".bin")

# [
#     {
#         "id": int,
#         "is_online": bool,
#         "max_alunos": int,
#         "data_ini": datetime,
#         "duracao_semanas": int,
#         "horario": tuple[hora_ini: int, hora_fim: int]
#     },
#     ...
# ]
# OBS: Os datetimes são armazenados como strings no formato ISO no json
_turmas: list[dict] = []

# Funções internas
def _gera_novo_id() -> int:
    """
    Gera sequencialmente um novo ID único, para uma nova instância de dicionário

    Utiliza o arquivo especificado em ID_FILE_PATH para guardar o próximo ID que deve ser gerado

    Cria os arquivos e diretórios necessários caso não existam

    Retorna -1 caso ocorra um erro de I/O ao ler ou escrever o arquivo de ID
    """
    if not os.path.isdir(_DATA_DIR_PATH):
        os.makedirs(_DATA_DIR_PATH)

    if not os.path.exists(_ID_FILE_PATH):
        id_atual = 1
    else:
        try:
            with open(_ID_FILE_PATH, 'r') as file:
                id_atual = int(file.read())
        except Exception as e:
            print(f"Erro de I/O em gera_novo_id: {e}")
            return -1

    id_proximo = id_atual + 1

    try:
        with open(_ID_FILE_PATH, 'w') as file:
            file.write(str(id_proximo))
    except Exception as e:
        print(f"Erro de I/O em gera_novo_id: {e}")
        return -1

    return id_atual

def _read_turmas() -> None:
    """
    Descompacta o arquivo .bin em _TURMAS_BIN_FILE_PATH, lê o arquivo .json resultante em _TURMAS_JSON_FILE_PATH
    e armazena o conteúdo em _turmas, uma lista de dicionários

    Se não existir, chama _write_turmas parar criar um novo vazio
    """
    global _turmas

    if not os.path.exists(_TURMAS_BIN_FILE_PATH):
        _write_turmas()
        return

    # Descompactação
    subprocess.run([_COMPACTADOR_PATH, _TURMAS_BIN_FILE_PATH])

    try:
        with open(_TURMAS_JSON_FILE_PATH, 'r') as file:
            _turmas = json.load(file)
    except Exception as e:
        print(f"Erro de I/O em _read_turmas: {e}")

    # Aqui deveríamos deletar o .json, mas vamos manter para fins de debug
    # os.remove(_TURMAS_JSON_FILE_PATH)

def _write_turmas() -> None:
    """
    Realiza o dump da lista _turmas para um arquivo json, definido em _TURMAS_JSON_FILE_PATH,
    e depois o compacta para um arquivo .bin usando o compactador em _COMPACTADOR_PATH

    Cria os arquivos necessários caso não existam, gerando uma lista vazia de turmas
    """
    if not os.path.isdir(_DATA_DIR_PATH):
        os.makedirs(_DATA_DIR_PATH)

    try:
        with open(_TURMAS_JSON_FILE_PATH, 'w') as file:
            json.dump(_turmas, file, indent=2)
    except Exception as e:
        print(f"Erro de I/O em _write_turmas: {e}")

    # Compactação
    subprocess.run([_COMPACTADOR_PATH, _TURMAS_JSON_FILE_PATH])

    # Aqui deveríamos deletar o .json, mas vamos manter para fins de debug
    # os.remove(_TURMAS_JSON_FILE_PATH)

def _horario_valido(horario: tuple[int, int]) -> bool:
    """
    Checa se um horário de aula é válido

    Deve estar entre 0 e 23, e a hora inicial deve ser menor que a final
    """
    if not isinstance(horario, tuple) or len(horario) != 2:
        return False

    hora_ini, hora_fim = horario

    if not isinstance(hora_ini, int) or not isinstance(hora_fim, int):
        return False

    if hora_ini < 0 or hora_ini > 23 or hora_fim < 0 or hora_fim > 23:
        return False
    
    if hora_ini >= hora_fim:
        return False

    return True

# Funções de acesso
def get_turma(id_turma: int) -> tuple[int, dict]:
    """
    Retorna o dicionário com os atributos da turma especificada
    """
    for turma in _turmas:
        if turma["id"] == id_turma:
            return 0, copy.deepcopy(turma)

    # Turma não encontrada
    return 1, None # type: ignore

def get_turmas() -> tuple[int, list[dict]]:
    """
    Retorna uma lista com todos os dicionários contendo os atributos de cada turma
    """
    return 0, copy.deepcopy(_turmas)

def set_max_alunos(id_turma: int, novo_max: int) -> tuple[int, dict]:
    """
    Altera o atributo max_alunos da turma especificada pelo ID

    Retorna o dicionário modificado da turma, ou None se houver algum erro
    """
    if novo_max < 1 or novo_max > 100:
        # Novo max_alunos inválido
        return 2, None # type: ignore

    for turma in _turmas:
        if turma["id"] == id_turma:
            if turma["is_online"]:
                # Não podemos alterar o max_alunos de uma turma online
                return 3, None # type: ignore

            turma["max_alunos"] = novo_max
            return 0, copy.deepcopy(turma)
    
    # Turma não encontrada
    return 1, None # type: ignore


def add_turma(is_online: bool, duracao: int, horario: tuple[int, int]) -> tuple[int, int]:
    """
    Cria uma nova proposta de turma com os atributos especificados
    
    Retorna o ID da nova turma
    """
    if not is_online and not _horario_valido(horario):
        # Horário inválido
        return 9, None # type: ignore
    
    if duracao < 1 or duracao > 53:
        # Duração inválida
        return 10, None # type: ignore
    
    novo_id = _gera_novo_id()
    if novo_id == -1:
        # Erro ao gerar o ID
        return 8, None # type: ignore
    
    nova_turma = {
        "id": novo_id,
        "is_online": is_online,
        "max_alunos": 10,
        "data_ini": None,
        "duracao_semanas": duracao,
        "horario": None if is_online else horario
    }

    _turmas.append(nova_turma)

    return 0, novo_id

def del_turma(id_turma: int) -> tuple[int, None]:
    """
    Remove uma proposta de turma pelo seu ID
    """
    for turma in _turmas:
        if turma["id"] == id_turma:
            _turmas.remove(turma)
            return 0, None
    
    # Turma não encontrada
    return 1, None

def is_final(id_turma: int) -> tuple[int, bool]:
    """
    Documentação
    """
    raise NotImplementedError

def is_ativa(id_turma: int) -> tuple[int, bool]:
    """
    Documentação
    """
    raise NotImplementedError

def abre_turma(id_turma: int) -> tuple[int, None]:
    """
    Atribui uma data de início para uma turma, tornando-a final e ativa,
    efetivamente inciando as aulas
    """
    for turma in _turmas:
        if turma["id"] == id_turma:
            if turma["data_ini"] is not None:
                # Turma já foi aberta
                return 11, None
            
            turma["data_ini"] = datetime.datetime.now()
            return 0, None
    
    # Turma não encontrada
    return 1, None

# Setup
# Popular lista de turmas
_read_turmas()

# Salvar turmas ao final do programa
atexit.register(_write_turmas)

# Isso executa quando turma.py é executado diretamente, mas não quando importado
# Testes iniciais podem ser feitos aqui
if __name__ == "__main__":
    pass
