import unittest, datetime
from turma import *

# Mock das turmas
_turmas = [
    {"id": 1, "is_online": False, "max_alunos": 10, "data_ini": datetime.datetime.now(), "duracao_semanas": 10, "horario": [9, 17]},
    {"id": 2, "is_online": True, "max_alunos": -1, "data_ini": None, "duracao_semanas": 5, "horario": None}
]

class TesteFuncoesTurma(unittest.TestCase):
    def teste_get_turma_nao_encontrada(self):
        resultado = get_turma(999)
        self.assertEqual(resultado, (1, None))

    def teste_get_turmas(self):
        resultado = get_turmas()
        self.assertEqual(resultado[0], 0)
        self.assertIsInstance(resultado[1], list)

    def teste_set_max_alunos_invalido(self):
        resultado = set_max_alunos(1, 101)
        self.assertEqual(resultado, (2, None))

    def teste_set_max_alunos_online(self):
        resultado = set_max_alunos(2, 20)
        self.assertEqual(resultado, (3, None))

    def teste_set_max_alunos_nao_encontrado(self):
        resultado = set_max_alunos(999, 20)
        self.assertEqual(resultado, (1, None))

    def teste_add_turma_horario_invalido(self):
        resultado = add_turma(False, 10, [24, 25])
        self.assertEqual(resultado, (9, None))

    def teste_add_turma_duracao_invalida(self):
        resultado = add_turma(False, 54, [10, 12])
        self.assertEqual(resultado, (10, None))

    def teste_del_turma_nao_encontrada(self):
        resultado = del_turma(999)
        self.assertEqual(resultado, (1, None))

    def teste_is_final_nao_encontrado(self):
        resultado = is_final(999)
        self.assertEqual(resultado, (1, None))

    def teste_is_ativa_nao_encontrada(self):
        resultado = is_ativa(999)
        self.assertEqual(resultado, (1, None))

    def teste_abre_turma_ja_aberta(self):
        abre_turma(1)
        resultado = abre_turma(1)
        self.assertEqual(resultado, (11, None))

    def teste_abre_turma_nao_encontrada(self):
        resultado = abre_turma(999)
        self.assertEqual(resultado, (1, None))

if __name__ == '__main__':
    unittest.main()