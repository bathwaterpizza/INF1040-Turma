import os, json, subprocess

# Funções de acesso
# O módulo deve ser importado com "from turma import *", e não "import turma"
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
    Documentação
    """
    raise NotImplementedError

def get_turmas() -> tuple[int, list[dict]]:
    """
    Documentação
    """
    raise NotImplementedError

def set_max_alunos(id_turma: int, novo_max: int) -> tuple[int, dict]:
    """
    Documentação
    """
    raise NotImplementedError

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

# Isso executa quando turma.py é executado diretamente, mas não quando importado
if __name__ == "__main__":
    import atexit

    # Ler turmas ao início do programa
    _read_turmas()

    # Testes iniciais podem ser feitos aqui
    # ...

    # Salvar turmas ao final do programa
    atexit.register(_write_turmas)