import os, json, subprocess

# Declarando as funções de acesso
# Devem ser importadas com "from turma import *", e não "import turma"
__all__ = ["get_turma", "get_turmas", "set_max_alunos", "add_turma", "del_turma", "is_final", 
           "is_ativa", "notify_novo_professor"]

# Globais
_turmas: list[dict] = []

# Constantes
_DATA_PATH: str = "data_turma"
_ID_FILE_PATH: str = os.path.join(_DATA_PATH, "proximo_id.txt")
_TURMAS_JSON_FILE_PATH: str = os.path.join(_DATA_PATH, "turmas.json")
_TURMAS_BIN_FILE_PATH: str = os.path.join(_DATA_PATH, "turmas.bin")

# Funções internas
def gera_novo_id() -> int:
    """
    Gera sequencialmente um novo ID único, para uma nova instância de dicionário

    Utiliza o arquivo especificado em ID_FILE_PATH para guardar o próximo ID que deve ser gerado

    Cria os arquivos necessários caso não existam: o diretório DATA_PATH e o arquivo ID_FILE_PATH
    """
    if not os.path.isdir(_DATA_PATH):
        os.makedirs(_DATA_PATH)
    
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

def read_turmas() -> None:
    """
    docstring
    """
    if not os.path.exists(_TURMAS_BIN_FILE_PATH):
        write_turmas()
        return
    
    pass

def write_turmas() -> None:
    """
    docstring
    """
    if not os.path.isdir(_DATA_PATH):
        os.makedirs(_DATA_PATH)

    try:
        with open(_TURMAS_JSON_FILE_PATH, 'w') as file:
            json.dump(_turmas, file, indent=4)
    except Exception as e:
        print(f"Erro de I/O em write_turmas: {e}")
    
    # Compactação
    subprocess.run(["./compactador.exe", _TURMAS_JSON_FILE_PATH])

    # Aqui deveríamos deletar o .json, mas vamos manter para fins de debug
    # os.remove(_TURMAS_JSON_FILE_PATH)

# Funções de acesso
def get_turma(id_turma: int) -> tuple[int, dict]:
    raise NotImplementedError

def get_turmas() -> tuple[int, list[dict]]:
    raise NotImplementedError

def set_max_alunos(id_turma: int, novo_max: int) -> tuple[int, dict]:
    raise NotImplementedError

def add_turma(id_curso: int, is_online: bool, horario: tuple[int, int]) -> tuple[int, int]:
    raise NotImplementedError

def del_turma(id_turma: int) -> tuple[int, None]:
    raise NotImplementedError

def is_final(id_turma: int) -> tuple[int, bool]:
    raise NotImplementedError

def is_ativa(id_turma: int) -> tuple[int, bool]:
    raise NotImplementedError

def notify_novo_professor(id_turma: int) -> tuple[int, None]:
    raise NotImplementedError

# Isso executa quando turma.py é executado diretamente, mas não quando importado
if __name__ == "__main__":
    # Ler turmas ao início
    read_turmas()

    # Salvar turmas ao final do programa
    import atexit
    atexit.register(write_turmas)