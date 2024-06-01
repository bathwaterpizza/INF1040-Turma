import os

# Declarando as funções de acesso
__all__ = []

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
    raise NotImplementedError()

def write_turmas() -> None:
    raise NotImplementedError()


# Isso executa quando turma.py é executado diretamente, e não quando importado
if __name__ == "__main__":
    # Salvar turmas ao final do programa
    import atexit
    atexit.register(write_turmas)