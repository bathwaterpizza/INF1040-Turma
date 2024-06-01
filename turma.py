import os

# Declarando as funções de acesso
__all__ = ["get_turma", "get_turmas", "set_max_alunos", "add_turma", "del_turma", "is_final", 
           "is_ativa", "notify_novo_professor"]

# Globais
_turmas: list[dict] = []

# Constantes
_DATA_PATH: str = "data_turma"
_ID_FILE_PATH: str = os.path.join(_DATA_PATH, "proximo_id.txt")

# Funções internas
def gera_novo_id() -> int:
    """
    Gera sequencialmente um novo ID único, para uma nova instância de dicionário

    Utiliza o arquivo especificado em ID_FILE_PATH para guardar o próximo ID que deve ser gerado

    Cria os arquivos necessários caso não existam: o diretório DATA_PATH e o arquivo ID_FILE_PATH
    """
    if not os.path.exists(_DATA_PATH):
        os.makedirs(_DATA_PATH)
    
    if not os.path.exists(_ID_FILE_PATH):
        id_atual = 1
    else:
        with open(_ID_FILE_PATH, 'r') as file:
            id_atual = int(file.read())

    id_proximo = id_atual + 1

    with open(_ID_FILE_PATH, 'w') as file:
            file.write(str(id_proximo))
    
    return id_atual

def read_turmas() -> None:
    raise NotImplementedError

def write_turmas() -> None:
    raise NotImplementedError

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

# Isso executa quando turma.py é executado diretamente, e não quando importado
if __name__ == "__main__":
    # Ler turmas ao início
    read_turmas()

    # Salvar turmas ao final do programa
    import atexit
    atexit.register(write_turmas)