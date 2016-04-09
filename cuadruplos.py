from structs import *
from cubosemantico import *
from tablas import *
from dmcparser import *
import sys

pilaO = Stack()
POper = Stack()
pTipos = Stack()
pSaltos = Stack()

# Inicia con el index 0
cuadruplos = []

# Inicia con el index 0
contSaltos = 0

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
	global contSaltos

	cuadruplos.append(cuadruplo)
	contSaltos+=1

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
	4. Si top(POper) == '*' o '/'
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
def exp_5(dirGlobal,dirActual):
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
	8. Meter AND/OR en POper
	============================================
'''
def exp_8(and_or):
	global POper
	POper.push(and_or)


'''
	=====================================================
	9. Si top(POper) es and o or , sacar and/or de POper
	=====================================================
'''
def exp_9():
	global POper
	global pTipos
	global pilaO
	
	#printPilas()
	if not POper.isEmpty():
		if POper.peek() == 'and' or POper.peek() == 'or':
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
				pTipos.push(tipoRes)
				pilaO.push(temp)
			else:
				sys.exit("Error. Tipos Incompatibles.")

'''
	============================================
	10. Meter < <= > >= <> == en POper
	============================================
'''
def exp_10(oper_logic):
	global POper
	POper.push(oper_logic)


'''
	=====================================================
	11. Si top(POper) es < <= > >= <> == , sacar de POper
	====================================================
'''
def exp_11():
	global POper
	global pTipos
	global pilaO
	
	#printPilas()
	if not POper.isEmpty():
		if POper.peek() == '<' or POper.peek() == '<=' or POper.peek() == '>' or POper.peek() == '>=' or POper.peek() == '<>' or POper.peek() == '==':
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
				pTipos.push(tipoRes)
				pilaO.push(temp)
			else:
				sys.exit("Error. Tipos Incompatibles.")


'''
	============================================
	12. Meter = en POper
	============================================
'''
def exp_12(asignOper):
	global POper
	POper.push(asignOper)


'''
	============================================
	13. Si top(POper) es = , sacar = de POper
	============================================
'''
def exp_13():
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
	============================================
	Estatuto PRINT
	============================================
'''
def estatuto_print():
	global pilaO
	global pTipos

	res = pilaO.pop()
	pTipos.pop()
	genera_cuadruplo = Cuadruplo("print", "", "", res)
	push_cuadruplo(genera_cuadruplo)

'''
	============================================
	Estatuto IF 1
	============================================
'''
def estatuto_if_1():
	global pilaO
	global pTipos
	global pSaltos

	auxTipo = pTipos.pop()
	if auxTipo != "bool":
		sys.exit("Error Semantico.")
	else:
		res = pilaO.pop()
		genera_cuadruplo = Cuadruplo("GOTOF", res, "", "")
		push_cuadruplo(genera_cuadruplo)
	pSaltos.push(contSaltos-1)



'''
	============================================
	Estatuto ELSE
	============================================
'''
def estatuto_else():
	global pilaO
	global pTipos
	global cuadruplos
	global pSaltos

	genera_cuadruplo = Cuadruplo("GOTO", "", "", "")
	push_cuadruplo(genera_cuadruplo)
	falso = pSaltos.pop()
	cuadruplos[falso].res = contSaltos
	pSaltos.push(contSaltos-1)

'''
	============================================
	Estatuto ENDIF
	============================================
'''
def estatuto_endif():
	global pilaO
	global pTipos
	global cuadruplos
	global pSaltos

	fin = pSaltos.pop()
	cuadruplos[fin].res = contSaltos

'''
	============================================
	Estatuto WHILE 1
	============================================
'''
def estatuto_while_1():
	global pSaltos

	pSaltos.push(contSaltos)

'''
	============================================
	Estatuto WHILE 2
	============================================
'''
def estatuto_while_2():
	global pilaO
	global pTipos
	global pSaltos

	auxTipo = pTipos.pop()
	if auxTipo != "bool":
		sys.exit("Error Semantico.")
	else:
		res = pilaO.pop()
		genera_cuadruplo = Cuadruplo("GOTOF", res, "", "")
		push_cuadruplo(genera_cuadruplo)
	pSaltos.push(contSaltos-1)

'''
	============================================
	Estatuto WHILE 3
	============================================
'''
def estatuto_while_3():
	global pSaltos

	falso = pSaltos.pop()
	retorno = pSaltos.pop()

	genera_cuadruplo = Cuadruplo("GOTO", "", "", retorno)
	push_cuadruplo(genera_cuadruplo)

	cuadruplos[falso].res = contSaltos

'''
	=========================================================
	Regresa numero del cuadruplo en el que inicia la funcion
	=========================================================
'''
def altaInicioFunc():
	global contSaltos
	return contSaltos

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
	print "PilaO ", pilaO.getElements()
	print "pTipos ", pTipos.getElements()
	print "POper ", POper.getElements()
	print "pSaltos ", pSaltos.getElements()
	print_cuadruplos(cuadruplos)

def print_cuadruplos(currentCuadList):
	print "Tabla Cuadruplos"
	index = 0
	for currentCuad in currentCuadList:
		if currentCuad:
			print index, " " ,currentCuad.op, " , ", currentCuad.opdoIzq, " , ", currentCuad.opdoDer," , ",currentCuad.res
		else:
			print "List is empty"
		index += 1
	pass
