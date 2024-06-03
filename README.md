# Como utilizar

No diretório imediatamente acima do seu módulo, execute:

`git clone https://github.com/bathwaterpizza/turma`

Depois você pode utilizar as funções de turma com o import:

```Python
from .. import turma

turma.get_turma(25)
```

**OBS:** Para utilizar imports relativos, seu módulo também precisa fazer parte de um package, ou seja, o diretório pai deve possuir um arquivo `__init__.py`

## add_turma

Essa função é chamada pelo aluno-turma quando ele determina que uma nova turma deve ser criada, para um aluno desejando se matricular em um curso.

O aluno-turma deve também inserir essa nova turma no módulo curso-turma, para definir o assunto lecionado na turma.

Nos checks de horário, as turmas com is_online == True são exceção, pois a turma online não possui horário fixo das aulas, como o conteúdo fica disponível offline.

## del_turma

Essa função é chamada pelo módulo aluno-turma, quando a turma esvazia. O aluno-turma deve se certificar que a turma está realmente vazia.

Isso acontece quando todos alunos estão inscritos há mais de uma semana, e então são movidos para uma turma online.

O aluno-turma deve também remover essa nova turma do módulo curso-turma.
