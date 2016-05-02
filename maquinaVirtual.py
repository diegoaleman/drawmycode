from structs import *
from dmcparser import *
from cuadruplos import *
from Memoria import *
from copy import deepcopy
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

temporalActual = 0
cuadruplo_actual = 0

dirproc = []
memGlobal = []
memActiva = []
memPasada = []
memCtes = []
cuadruplos = []
pila = []
listaParams = []
funcionActual = 'main'
funcionPasada = ''
params = 0
existeRetorno = False
valorRetorno = []

def initMaquinaVirtual(dProc, mGlobal, mActiva, mCtes, cuads):
	global memCtes
	global memGlobal
	global memActiva
	global cuadruplos
	global dirproc
	dirproc = dProc
	memCtes = mCtes
	memGlobal = mGlobal
	memActiva = mActiva
	cuadruplos = cuads
	print len(cuads)
	main()



		



def getValue(direccion):
	if direccion>=1 and direccion<4000: #LOCAL
		return memGlobal.get_valor_memoria(direccion)
	if direccion>=4000 and direccion<8000: #GLOBAL
		return memActiva.get_valor_memoria(direccion)
	if direccion>=8000 and direccion<12000: #TEMPORAL
		return memActiva.get_valor_memoria(direccion)
	if direccion>=12000 and direccion<16000: #CONSTANTE
		return memCtes.get_valor_memoria(direccion)


def setValue(valor, direccion):
	if direccion>=1 and direccion<4000: #LOCAL
		return memGlobal.set_valor_memoria(valor, direccion)
	if direccion>=4000 and direccion<8000: #GLOBAL
		return memActiva.set_valor_memoria(valor, direccion)
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
	if op == 'GOTO':
		return goto
	if op == 'ERA':
		return era
	if op == 'GOSUB':
		return gosub
	if op == 'PARAM':
		return param
	if op == 'RET':
		return ret
	if op == 'RETURN':
		return retorno
	if op == 'LINE':
		return line


'''
=========================================================

Corregir el valor que va a asignar, puede ser booleano, 
cambiar el float

=========================================================
'''
def asignacion(c1, c2, c3):
	global existeRetorno
	global valorRetorno

	if existeRetorno == True:
		existeRetorno = False
		setValue(valorRetorno.pop(), c3)
	else:
		value = float(getValue(c1))
		setValue(value, c3)

	print "asign"	
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
def goto(c1, c2, c3):
	global cuadruplo_actual
	cuadruplo_actual = c3

def era(c1, c2, c3):
	global pila
	global cuadruplo_actual
	global memActiva
	global memPasada
	global funcionActual
	global funcionPasada
	global dirproc
	global params

	params = 0
	funcionPasada = funcionActual
	funcionActual = c2
	memPasada = deepcopy(memActiva)
	memActiva = Memoria(dirproc[c2]['Tamano']['ints'],dirproc[c2]['Tamano']['floats'],dirproc[c2]['Tamano']['strings'],dirproc[c2]['Tamano']['bools'],dirproc[c2]['Tamano']['tempInts'],dirproc[c2]['Tamano']['tempFloats'], dirproc[c2]['Tamano']['tempStrings'], dirproc[c2]['Tamano']['tempBools'])

def param(c1, c2, c3):
	global params
	asignacion(c1,c2,c3)
	params = params + 1

def gosub(c1, c2, c3):
	global params
	global cuadruplo_actual
	global pila
	global memPasada
	global funcionPasada
	global dirproc
	global memActiva

	if params == len(dirproc[c1]['OrderedParams']):
		pila.append([cuadruplo_actual, funcionPasada, memPasada])
		params = 0
		cuadruplo_actual = c3
	else:
		print 'Numero incorrecto de parametros en funcion'
		sys.exit()


def ret(c1, c2, c3):
	global memActiva
	global cuadruplo_actual
	global funcionActual
	
	p = pila.pop()
	memActiva = p[2]

	funcionActual = p[1]
	cuadruplo_actual = p[0]

def retorno(c1, c2, c3):
	global valorRetorno
	global existeRetorno

	existeRetorno = True
	valorRetorno.append(getValue(c3))


def line(c1, c2, c3):
	x1 = getValue(c1[0])
	y1 = getValue(c1[1])
	x2 = getValue(c1[2])
	y2 = getValue(c1[3])
	print "LINEA"
	print x1
	print y1
	print x2
	print y2
	
	glColor3ub(255, 0, 0)
	glBegin(GL_LINES);
	glVertex3f(float(x1), float(y1),0.0)
	glVertex3f(float(x2), float(y2),0.0)
	glEnd()
	

def myKeyboard(key, x, y):
	if key == 'q':
		sys.exit()

window = 0                                             # glut window number
width, height = 500, 400   

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-width, width, -height, height, 0.0, 100.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw():                           # set color to white
	glutSwapBuffers() 

def main():
	global cuadruplo_actual
	glutInit(sys.argv)
	glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize (500, 500)
	glutInitWindowPosition (100, 100)
	glutCreateWindow ('DRAWMYCODE')
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
	glLoadIdentity()  
	refresh2d(width, height)                      
	glColor3f(1.0, 1.0, 1.0)

	print "----------------------"
	cuadruplos_totales = len(cuadruplos)
	while cuadruplo_actual < cuadruplos_totales:
		currentCuad = cuadruplos[cuadruplo_actual]
		cuadruplo_actual =  cuadruplo_actual + 1

		print currentCuad.op, currentCuad.opdoIzq, currentCuad.opdoDer, currentCuad.res

		if currentCuad.op == '+'  or currentCuad.op == '=' or currentCuad.op == '*' or currentCuad.op == '-' or currentCuad.op == '/' or currentCuad.op == '>' or currentCuad.op == '<' or currentCuad.op == '<>' or currentCuad.op == '==' or currentCuad.op == '>=' or currentCuad.op == '<=' or currentCuad.op == 'GOTOF' or currentCuad.op == 'GOTO'  or currentCuad.op == 'ERA'  or currentCuad.op == 'GOSUB' or currentCuad.op == 'PARAM' or currentCuad.op == 'RET' or currentCuad.op == 'RETURN' or currentCuad.op == 'LINE':
			metodo = getMetodo(currentCuad.op)
			metodo(currentCuad.opdoIzq, currentCuad.opdoDer, currentCuad.res)
		

	glutKeyboardFunc(myKeyboard)
	glutDisplayFunc(draw)
	glutIdleFunc(draw)
	glutMainLoop()



	
	exit(-1)

