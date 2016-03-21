from structs import *
pilaO = Stack()
POper = Stack()
pTipos = Stack()
cuadruplos = []

class Cuadruplo:

  def __init__(self, operador, operandoIzq, operandoDer, temp):
		self.op = operador
		self.opdoIzq = operandoIzq
		self.opdoDer = operandoDer
		self.res = temp

def exp_1(dirvar,tipo):

	global pilaO
	global pTipos

	pilaO.push(dirvar)
	pTipos.push(tipo)


def printPilas():
	print pilaO.getElements()
	print pTipos.getElements()
	print POper.getElements()

def exp_2(product_division):
	global POper
	POper.push(product_division)

def exp_3(plus_minus):
	global POper
	POper.push(plus_minus)

def exp_4():
	global POper
	if not POper.isEmpty:
		if POper.peek() == '*' or POper.peek() == '/':
			op = POper.pop()
			if not pilaO.isEmpty:
				opdoDer = pilaO.pop()
			if not pilaO.isEmpty:
				opdoIzq = pilaO.pop()
				genera_cuadruplo = Cuadruplo(op,opdoIzq,opdoDer,temp)
