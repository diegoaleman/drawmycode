from structs import *
from dmcparser import *
from cuadruplos import *
import sys

tablaConstantes = {}
temporalActual = 0
varTemporales = [1000]

def initMaquinaVirtual(t):
	tablaConstantes = t.copy()
	global tablaConstantes
	main()


def main():
	print "----------------------"
	cuadruplo_actual = 0
	for currentCuad in cuadruplos:
		if currentCuad.op == '+':
			#print tablaConstantes
			suma(2001,2001,2001)
			#suma(currentCuad.opdoIzq, currentCuad.opdoDer, currentCuad.res)
		cuadruplo_actual += 1
	pass

	print "*Cantidad de cuadruplos"
	print cuadruplo_actual

	print varsGlobalesDir


	
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



