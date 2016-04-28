from structs import *
from dmcparser import *
from cuadruplos import *
from Memoria import *
import sys

temporalActual = 0
cuadruplo_actual = 0

memGlobal = []
memActiva = []
memCtes = []
cuadruplos = []

def initMaquinaVirtual(mGlobal, mActiva, mCtes, cuads):
	global memCtes
	global memGlobal
	global memActiva
	global cuadruplos
	memCtes = mCtes
	memGlobal = mGlobal
	memActiva = mActiva
	cuadruplos = cuads
	main()

def main():
	global cuadruplo_actual
	print "----------------------"
	cuadruplos_totales = len(cuadruplos)
	while cuadruplo_actual < cuadruplos_totales:

		currentCuad = cuadruplos[cuadruplo_actual]

		print currentCuad.op, currentCuad.opdoIzq, currentCuad.opdoDer, currentCuad.res

		if currentCuad.op == '+'  or currentCuad.op == '=' or currentCuad.op == '*' or currentCuad.op == '-' or currentCuad.op == '/' or currentCuad.op == '>' or currentCuad.op == '<' or currentCuad.op == '<>' or currentCuad.op == '==' or currentCuad.op == '>=' or currentCuad.op == '<=' or currentCuad.op == 'GOTOF':
			metodo = getMetodo(currentCuad.op)
			metodo(currentCuad.opdoIzq, currentCuad.opdoDer, currentCuad.res)

		cuadruplo_actual =  cuadruplo_actual + 1


	'''
	for currentCuad in cuadruplos:
			 
			metodo = getMetodo(currentCuad.op)
			metodo(currentCuad.opdoIzq, currentCuad.opdoDer, currentCuad.res)
		
		cuadruplo_actual += 1
		if currentCuad.op == '+':
			suma(currentCuad.opdoIzq, currentCuad.opdoDer, currentCuad.res)
			'''

def getValue(direccion):
	if direccion>=1 and direccion<4000: #LOCAL
		return memActiva.get_valor_memoria(direccion)
	if direccion>=4000 and direccion<8000: #GLOBAL
		return memGlobal.get_valor_memoria(direccion)
	if direccion>=8000 and direccion<12000: #TEMPORAL
		return memActiva.get_valor_memoria(direccion)
	if direccion>=12000 and direccion<16000: #CONSTANTE
		return memCtes.get_valor_memoria(direccion)


def setValue(valor, direccion):
	if direccion>=1 and direccion<4000: #LOCAL
		return memActiva.set_valor_memoria(valor, direccion)
	if direccion>=4000 and direccion<8000: #GLOBAL
		return memGlobal.set_valor_memoria(valor, direccion)
	if direccion>=8000 and direccion<12000: #TEMPORAL
		return memActiva.set_valor_memoria(valor, direccion)
	if direccion>=12000 and direccion<16000: #CONSTANTE
		return memCtes.set_valor_memoria(valor, direccion)


def getMetodo(op):
	if op == '=':
		return asignacion 
	if op == '+':
		return suma
	if op == '-':
		return resta
	if op == '*':
		return multiplicacion
	if op == '/':
		return division
	if op == '>':
		return greater_than
	if op == '<':
		return less_than
	if op == '<>':
		return different
	if op == '==':
		return equal
	if op == '>=':
		return greater_equal_than
	if op == '<=':
		return less_equal_than
	if op == 'GOTOF':
		return gotof


'''
=========================================================

Corregir el valor que va a asignar, puede ser booleano, 
cambiar el float

=========================================================
'''
def asignacion(c1, c2, c3):
	print "asign"
	value = float(getValue(c1))
	setValue(value, c3)
	print getValue(c3)

def suma(c1, c2, c3):
	value = float(getValue(c1)) + float(getValue(c2))
	setValue(value, c3)

def resta(c1, c2, c3):
	value = float(getValue(c1)) - float(getValue(c2))
	setValue(value, c3)

def multiplicacion(c1, c2, c3):
	value = float(getValue(c1)) * float(getValue(c2))
	setValue(value, c3)

def division(c1, c2, c3):
	value = float(getValue(c1)) / float(getValue(c2))
	setValue(value, c3)

def greater_than(c1, c2, c3):
	value = float(getValue(c1)) > float(getValue(c2))
	setValue(value, c3)

def less_than(c1, c2, c3):
	value = float(getValue(c1)) < float(getValue(c2))
	setValue(value, c3)

def different(c1, c2, c3):
	value = float(getValue(c1)) != float(getValue(c2))
	setValue(value, c3)

def equal(c1, c2, c3):
	value = float(getValue(c1)) == float(getValue(c2))
	setValue(value, c3)

def greater_equal_than(c1, c2, c3):
	value = float(getValue(c1)) >= float(getValue(c2))
	setValue(value, c3)

def less_equal_than(c1, c2, c3):
	value = float(getValue(c1)) <= float(getValue(c2))
	setValue(value, c3)

def gotof(c1, c2, c3):
	global cuadruplo_actual
	value = getValue(c1)
	if value == False:
		cuadruplo_actual = c3



	'''

def setValue():
	return 1

#return memActiva.get_valor_memoria(tipo, direccion)




getTipo(direccion):
	if direccion>=1 and direccion<4000:
		if tipo=='int':
			return 1
		if tipo=='float':
			return 1000
		if tipo=='bool':
			return 2000
		if tipo=='string':
			return 3000
	if direccion>=4000 and direccion<8000:
		if tipo=='int':
			return 4000
		if tipo=='float':
			return 5000
		if tipo=='bool':
			return 6000
		if tipo=='string':
			return 7000
	if direccion>=8000 and direccion<12000:
		if tipo=='int':
			return 8000
		if tipo=='float':
			return 9000
		if tipo=='bool':
			return 10000
		if tipo=='string':
			return 11000
	if direccion>=12000 and direccion<16000:
		if tipo=='int':
			return 12000
		if tipo=='float':
			return 13000
		if tipo=='bool':
			return 14000
		if tipo=='string':
			return 15000


'''
	



'''
	

				#suma(2001,2001,2001)
			#suma(currentCuad.opdoIzq, currentCuad.opdoDer, currentCuad.res)
			
				

				for key, elems in tablaConstantes.iteritems():
					direccion = elems['Dir']
					tipo = elems['Tipo']
					valor = key
					memCtes.set_valor_memoria(valor, tipo, direccion)








					#for key, elems in tablaConstantes:
	#	print key, elems
		#if elems['Dir'] == c1:
		#	print key


				
				memCtes.ints[0] = 4

				print "MEMORIA GLOBAL"
				print memCtes.ints[0]

				print memGlobal.tempInts[offset]
				print memActiva.tempInts
				print memCtes.strings
				'''









	
'''
def getEntConstante(c):
	for key, elems in tablaConstantes.iteritems():
		if elems['Dir'] == c:
			return key

def getEntTemp(c):
	return varTemporales[1000-c]


def getEntero(c):
	if c>=1 and c<=999:
		return getEntGL(c)
	elif c>=1000 and c<=1999:
		return getEntTemp(c)
	elif c>=2000 and c<=9999:
		return getEntConstante(c)
	else:
		return -1

def get(c):
	if c>=1 and c<=9999:
		return getEntero(c)
	elif c>=10000 and c<=19999:
		return getFloat(c)
	elif c>=20000 and c<=29000:
		return getBool(c)
	elif c<=30000 and c<= 39000:
		return getString(c)

def suma(c1,c2,c3):
	print "diego"
	varTemporales[1000-c3] = float(get(c1)) + float(get(c2))
	print varTemporales[1000-c3]

	#for key, elems in tablaConstantes:
	#	print key, elems
		#if elems['Dir'] == c1:
		#	print key



if currentCuad:
	print cuadruplo_actual, " " ,currentCuad.op, " , ", currentCuad.opdoIzq, " , ", currentCuad.opdoDer," , ",currentCuad.res
else:
	print "List is empty"


def getEntGL(c):

def getFloat(c):

def getBool(c):

def getString(c):

'''
	#while cuadruplo_actual < len(cuadruplos):
	#	cuadruplo_actual += 1
	#print "diego"
	#print cuadruplo_actual 



