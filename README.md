# Como utilizar

No diretório imediatamente acima do seu módulo, execute:

`git clone https://github.com/bathwaterpizza/turma`

Depois você pode utilizar as funções de turma com o import:

```Python
from .. import turma

turma.get_turma(25)
```

**OBS:** Para utilizar imports relativos, seu módulo também precisa fazer parte de um package, ou seja, o diretório do módulo deve possuir um arquivo `__init__.py` assim como o nosso.

Alternativamente, se o diretório acima do seu módulo também for um repositório, como o principal, você pode adicionar turma como submódulo:

`git submodule add https://github.com/bathwaterpizza/turma`

## Dependências

Python 3.9+

# Documentação adicional

## add_turma

Essa função é chamada pelo aluno-turma, quando ele determina que uma nova turma deve ser criada, para um aluno desejando se matricular em um certo curso. 

O aluno-turma deve também inserir essa nova turma no módulo curso-turma, para definir o assunto lecionado na turma, e ainda no filial-turma, caso seja presencial, para definir onde acontecem as aulas.

### Requisitos
- Uma turma possui `10` vagas por padrão, exceto para turmas online, cujo `max_alunos` será `-1`.
- Estamos limitando a duração de uma turma para 53 semanas, aproximadamente um ano.
- Nos checks de horário, as turmas com is_online == True são exceção, pois a turma online não possui horário fixo das aulas.
  
### Acoplamento
- is_online: bool
  Variável usada para definir se uma turma é online ou não, na sua criação.
  
- duracao_semanas: int
  Define a duração de uma turma para sua criação.
  
-  horario: list(int)
  Uma lista de horários, com o horário de início e fim da turma. Usada para estabelecer o horário da proposta de turma que está sendo criada.

### Condições de acoplamento

- `horario` deve ser composto apenas por dois inteiros.
- `horario` deve ter ambos os inteiros entre 0 e 23.
- `hora_ini` deve ser menor que `hora_fim`.
- `duracao_semanas` deve estar entre 1 e 53.

## del_turma

Essa função é chamada pelo módulo aluno-turma, quando a proposta de turma esvazia de alunos. Isso acontece quando todos alunos ficaram inscritos há mais de uma semana, sem a turma abrir, e então foram movidos para uma turma online. 

O aluno-turma deve também remover essa nova turma do módulo curso-turma.

Assume-se que já foi verificado que a turma está realmente vazia.

### Requisitos

- Uma proposta de turma presencial se concretiza com o número de alunos estipulados para aquela turma e um professor para lecionar.
- Uma proposta de turma presencial que não se concretizou, passa a ser uma turma online.
  
### Acoplamento

- id_turma: int
  Função recebe o id da turma para poder acessar a turma que será excluída da lista de turmas.

## abre_turma

Essa função é chamada pelo principal, ou pelo professor-turma, quando uma turma está cheia e um professor assume a turma.

> Lembrando que um professor só pode assumir turmas cheias.

Ela atribui a data atual para data_ini da turma, o que efetivamente "abre" a mesma, tornando `is_final()` e `is_ativa()` verdadeiro para a turma.

Assume-se que, no caso da turma não ser online, já foi verificado que a turma está realmente cheia, e que um professor foi de fato alocado para a turma.

### Acoplamento

- id_turma: int
  Parâmetro usado para verificar se uma turma já foi aberta, caso contrário, usa o id para definir um horário de início da turma.

## is_final

Definimos uma turma finalizada como uma proposta de turma que foi aberta, mesmo se as aulas já terminaram.

No nosso caso, a turma está finalizada sempre que possuir uma data de início, pois nesse ponto já foi verificado pelo módulo aluno-turma que a turma está cheia, e pelo módulo professor-turma que um professor foi alocado, no caso da turma não ser online.

Se a turma for online, ela é considerada finalizada, ou aberta, assim que é criada.

### Acoplamento

- id_turma: int
  Recebe o id da turma para verificar se ela foi aberta.

### Condições de acoplamento

- Checa se o atributo `data_ini` da turma não é vazio, caso não seja, turma já foi aberta.

## is_ativa

Uma turma ativa é uma turma que está finalizada e que ainda não terminou.

Simplesmente verifica se a data inicial, somada com a duração das aulas da turma, é maior que a data atual.

### Acoplamento

- id_turma: int
  Recebe o id da turma para verificar se o tempo da turma já foi concluído a partir dos atributos `data_ini` e `duracao_semanas` da turma.
  
### Requisitos

- Todas as turmas tem 53 semanas de duração, sem exceção.
  
### Condições de acoplamento

- `data_ini` deve ser sempre menor que a data presente da checagem (Uma turma não é aberta em um ponto futuro).
- Caso o curso passe de sua duração máxima a partir de sua data de início, a turma foi aberta mas já terminou.

## get_turma

Retorna o dicionário com os atributos da turma especificada pelo id da turma.

Função usada pelos módulos aluno-turma e professor-turma, cria uma cópia do dicionário de turmas especificado pelo `id_turma`.

### Acoplamento

- id_turma: int
  Usa o id da turma para retornar uma cópia dos atributos dessa turma específica.

### Condições de acoplamento

- Se `id_turma` não exisitr, a turma não será encontrada.

## get_turmas

Retorna uma lista com o dicionário de todas as turmas e seus atributos.

Não necesita a entrada de nenhum parâmetro pois retorna todas as turmas, não uma específica diferente da função `get_turma`.

## set_max_alunos

Altera o atributo max_alunos, responsável pelo número de alunos necessários para concretizar a proposta de uma turma presencial, que tem como padrão 10 alunos.

### Acoplamento

- id_turma: int
  Usado para acessar atributos da turma com o id específico e conferir se ela é online.
  
- novo_max: int
  Inteiro que representa o novo número máximo de alunos que atualiza o atributo `max_alunos` da turma.

### Condições de acoplamento

- Caso a turma seja online, turma não tem número máximo de alunos.
- `novo_max` não pode ser menor que 1 e maior que 100.
