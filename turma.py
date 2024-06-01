import os

DATA_PATH = "data_turma"
ID_FILE_PATH = os.path.join(DATA_PATH, "proximo_id.txt")

def gerar_novo_id() -> int:
    """
    Gera sequencialmente um novo ID único, para uma nova instância de dicionário

    Utiliza o arquivo especificado em ID_FILE_PATH para guardar o próximo ID que deve ser gerado

    Cria os arquivos necessários caso não existam: o diretório DATA_PATH e o arquivo ID_FILE_PATH
    """
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
    
    if not os.path.exists(ID_FILE_PATH):
        id_atual = 1
    else:
        with open(ID_FILE_PATH, 'r') as file:
            id_atual = int(file.read())

    id_proximo = id_atual + 1

    with open(ID_FILE_PATH, 'w') as file:
            file.write(str(id_proximo))
    
    return id_atual
