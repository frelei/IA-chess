"""  
	CLASSE QUE REPRESENTARA O CAMPO DE XADREZ,
	DEVE RECEBER UMA STRING COMO PARAMETRo DA CONFIGURACAO ATUAL DO CAMPO,
	DEVE GERAR UMA MATRIZ BIDIMENSIONAL CONTENDO UM CHAR INDICANDO A PECA, 
"""

class Board:

	def __init__(self,fields):
		# Deve receber uma string para configurar
		self.field = filelds
		self.matrix = [[0 for x in xrange(8)] for x in xrange(8)] 

	def generate(self):
		print ('Implements please!!!!');		