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

O aluno-turma deve também inserir essa nova turma no módulo curso-turma, para definir o assunto lecionado na turma.

Nos checks de horário, as turmas com is_online == True são exceção, pois a turma online não possui horário fixo das aulas.

## del_turma

Essa função é chamada pelo módulo aluno-turma, quando a proposta de turma esvazia de alunos. Isso acontece quando todos alunos ficaram inscritos há mais de uma semana, sem a turma abrir, e então foram movidos para uma turma online.

O aluno-turma deve também remover essa nova turma do módulo curso-turma.

Assume-se que já foi verificado que a turma está realmente vazia.

## abre_turma

Essa função é chamada pelo principal, ou pelo professor-turma, quando uma turma está cheia e um professor assume a turma.

> Lembrando que um professor só pode assumir turmas cheias.

Ela atribui a data atual para data_ini da turma, o que efetivamente "abre" a mesma, tornando `is_final()` e `is_ativa()` verdadeiro para a turma.

Assume-se que, no caso da turma não ser online, já foi verificado que a turma está realmente cheia, e que um professor foi de fato alocado para a turma.

## is_final

Definimos uma turma finalizada como uma proposta de turma que foi aberta, mesmo se as aulas já terminaram.

No nosso caso, a turma está finalizada sempre que possuir uma data de início, pois nesse ponto já foi verificado pelo módulo aluno-turma que a turma está cheia, e pelo módulo professor-turma que um professor foi alocado, no caso da turma não ser online.

Se a turma for online, ela é considerada finalizada, ou aberta, assim que é criada.

## is_ativa

Uma turma ativa é uma turma que está finalizada e que ainda não terminou.

Simplesmente verifica se a data inicial, somada com a duração das aulas da turma, é maior que a data atual.
