from structs import *
from cubosemantico import *
from tablas import *
import sys

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
'''
	===================================================
	Inserta estructura Cuadruplo en lista de cuadruplos
	===================================================
'''
def push_cuadruplo(cuadruplo):
	global cuadruplos
	global cont_saltos

	cuadruplos.append(cuadruplo)

''' 
	============================================
	1. Meter direccion y tipo del ID en PilaO
	============================================
''' 
def exp_1(dirvar,tipo):
	global pilaO
	global pTipos

	pilaO.push(dirvar)
	pTipos.push(tipo)


''' 
	============================================
	2. Meter * o / en POper
	============================================
'''
def exp_2(product_division):
	global POper
	POper.push(product_division)


''' 
	============================================
	3. Meter + o - en POper
	============================================
'''
def exp_3(plus_minus):
	global POper
	POper.push(plus_minus)


''' 
	============================================
	4. Si top(POper) == '+' o '-'
	============================================
'''
def exp_4():
	global POper
	global pTipos
	global pilaO

	if not POper.isEmpty():
		if POper.peek() == '*' or POper.peek() == '/':
			op = POper.pop()

			opdoDer = pilaO.pop()
			tipoDer = pTipos.pop()

			opdoIzq = pilaO.pop()
			tipoIzq = pTipos.pop()

			tipoRes = cuboSemantico[tipoIzq][tipoDer][op];

			if tipoRes != "Error":
				temp = generaResDir(tipoRes)			
				
				genera_cuadruplo = Cuadruplo(op,opdoIzq,opdoDer,temp)
				push_cuadruplo(genera_cuadruplo)

				pilaO.push(temp)
				pTipos.push(tipoRes)
			else:
				sys.exit("Error. Tipos Incompatibles.")

'''
	============================================
	5. Si top(POper) == '+' o '-'
	============================================
'''
def exp_5():
	global POper
	global pTipos
	global pilaO

	if not POper.isEmpty():
		if POper.peek() == '+' or POper.peek() == '-':
			op = POper.pop()

			opdoDer = pilaO.pop()
			tipoDer = pTipos.pop()

			opdoIzq = pilaO.pop()
			tipoIzq = pTipos.pop()

			tipoRes = cuboSemantico[tipoIzq][tipoDer][op];

			if tipoRes != "Error":
				temp = generaResDir(tipoRes)			
				
				genera_cuadruplo = Cuadruplo(op,opdoIzq,opdoDer,temp)
				push_cuadruplo(genera_cuadruplo)

				pilaO.push(temp)
				pTipos.push(tipoRes)
			else:
				sys.exit("Error. Tipos Incompatibles.")

'''
	============================================
	6. Meter Fondo Falso en POper
	============================================
'''
def exp_6():
	global POper
	POper.push('[')

'''
	============================================
	7. Sacar Fondo Falso
	============================================
'''
def exp_7():
	global POper
	POper.pop()

'''
	============================================
	8. Meter = en POper
	============================================
'''
def exp_8(asignOper):
	global POper
	POper.push(asignOper)


'''
	============================================
	9. Si top(POper) es = , sacar = de POper
	============================================
'''
def exp_9():
	global POper
	global pTipos
	global pilaO
	
	if not POper.isEmpty():
		if POper.peek() == '=':
			op = POper.pop()

			opdoDer = pilaO.pop()
			tipoDer = pTipos.pop()

			res = pilaO.pop()
			tipoRes = pTipos.pop()

			

			revisaTipoRes = cuboSemantico[tipoRes][tipoDer][op];

			if revisaTipoRes != "Error":
							
				genera_cuadruplo = Cuadruplo(op,opdoDer,None,res)
				push_cuadruplo(genera_cuadruplo)
			else:
				sys.exit("Error. Tipos Incompatibles.")

'''
	=====================================================================
	Genera direccion para la respuesta de una operacion para un cuadruplo
	======================================================================
'''
def generaResDir(tipoRes):
	global contDirIntTemp
	global contDirFloatTemp
	global contDirBoolTemp
	global contDirStringTemp

	if tipoRes == "int":
		dirTemp  = contDirIntTemp
		contDirIntTemp +=1
	elif tipoRes == "float":
		dirTemp = contDirFloatTemp
		contDirFloatTemp +=1
	elif tipoRes == "bool":
		dirTemp = contDirBoolTemp
		contDirBoolTemp +=1
	elif tipoRes == "String":
		dirTemp = contDirStringTemp
		contDirStringTemp +=1
	return dirTemp

def printPilas():
	print pilaO.getElements()
	print pTipos.getElements()
	print POper.getElements()
	print_cuadruplos(cuadruplos)

def print_cuadruplos(currentCuadList):
	print "Tabla Cuadruplos"
	for currentCuad in currentCuadList:
		if currentCuad:
			print currentCuad.op, " , ", currentCuad.opdoIzq, " , ", currentCuad.opdoDer," , ",currentCuad.res
		else:
			print "List is empty"
	pass
