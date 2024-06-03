import os, json, subprocess, atexit 


# Funções de acesso
__all__ = ["get_turma", "get_turmas", "set_max_alunos", "add_turma", "del_turma", "is_final", 
           "is_ativa", "notify_novo_professor"]

# Globais
_SCRIPT_DIR_PATH: str = os.path.dirname(os.path.realpath(__file__))
_DATA_DIR_PATH: str = os.path.join(_SCRIPT_DIR_PATH, "data")
_COMPACTADOR_PATH: str = os.path.join(_SCRIPT_DIR_PATH, "compactador.exe")
_ID_FILE_PATH: str = os.path.join(_DATA_DIR_PATH, "proximo_id.txt")
_TURMAS_JSON_FILE_PATH: str = os.path.join(_DATA_DIR_PATH, "turmas.json")
_TURMAS_BIN_FILE_PATH: str = _TURMAS_JSON_FILE_PATH.replace(".json", ".bin")

_turmas: list[dict] = []

# Funções internas
def _gera_novo_id() -> int:
    """
    Gera sequencialmente um novo ID único, para uma nova instância de dicionário

    Utiliza o arquivo especificado em ID_FILE_PATH para guardar o próximo ID que deve ser gerado

    Cria os arquivos necessários caso não existam: o diretório DATA_PATH e o arquivo ID_FILE_PATH

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
    e armazena o conteúdo em _turmas, uma lista de dicionários.

    Se não existir, chama write_turmas parar criar um novo vazio
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
        print(f"Erro de I/O em read_turmas: {e}")

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
        print(f"Erro de I/O em write_turmas: {e}")

    # Compactação
    subprocess.run([_COMPACTADOR_PATH, _TURMAS_JSON_FILE_PATH])

    # Aqui deveríamos deletar o .json, mas vamos manter para fins de debug
    # os.remove(_TURMAS_JSON_FILE_PATH)

# Funções de acesso
def get_turma(id_turma: int) -> tuple[int, dict]:
    """
    A função recebe um ID de turma (int) e procura na lista de dicionários _turmas se existe um id igual.
    
    Caso exista, ele retorna o ID e o dicionário da turma desejada.
    
    Caso não uma mensagem é impressa pelo console.
    """
    for turma in _turmas:
        if turma["id"] == id_turma:
            return id_turma, turma

    
    raise ValueError(f"Turma com id {id_turma} não foi encontrada.")

def get_turmas() -> tuple[int, list[dict]]:
    """
    A função retorna uma o número total de turmas 
    e uma lista de dicionários com as turmas.
    
    Ele verificará se _turmas é uma lista de dicionários, 
    caso não retronará um erro.
    
    Caso ele não consiga encontrar _turmas, para encotrar len
    ele retornará um erro também.
    
    OBS: aparentemente se você retorna o dicionário em uma tupla,
    ele está protegido de alterações, pois tuplas são imutáveis. 
    (não tenho absolutamente certeza, isso foi oq o chat gpt me respondeu)
    
    Outra solução que ví foi usar a bilioteca copy, 
    que da para usar a função deepcopy que faz uma replica disto.
    """
    try:
        if not isinstance(_turmas, list):
            raise ValueError("A variável _turmas não é uma lista")
        if not all(isinstance(turma, dict) for turma in _turmas):
            raise ValueError("Nem todos os itens em _turmas são dicionários")

        n = len(_turmas)
    except TypeError:
        raise ValueError("Não foi possível encontrar _turmas")

    return n, _turmas

def set_max_alunos(id_turma: int, novo_max: int) -> tuple[int, dict]:
    """
    Função busca em turmas a turma com id desejado e altera
    o valor do dicionário de "max_alunos" para o novo valor
    guardado em novo_max. 

    Caso não encontre a turma, retorna um erro.
    """

    for turma in _turmas:
        if turma["id"] == id_turma:
            turma["max_alunos"] = novo_max
            return id_turma, turma

    
    raise ValueError(f"Turma com id {id_turma} não foi encontrada.")

def add_turma(id_curso: int, is_online: bool, horario: tuple[int, int]) -> tuple[int, int]:
    """
    Documentação
    """
    raise NotImplementedError

def del_turma(id_turma: int) -> tuple[int, None]:
    """
    Documentação
    """
    raise NotImplementedError

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

def notify_novo_professor(id_turma: int) -> tuple[int, None]:
    """
    Documentação
    """
    raise NotImplementedError

# Setup
# Popular lista de turmas
_read_turmas()

# Salvar turmas ao final do programa
atexit.register(_write_turmas)

# Isso executa quando turma.py é executado diretamente, mas não quando importado
# Testes iniciais podem ser feitos aqui
if __name__ == "__main__":
    pass