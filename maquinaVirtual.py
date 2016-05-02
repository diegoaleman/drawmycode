from structs import *
from dmcparser import *
from cuadruplos import *
from Memoria import *
from copy import deepcopy
import OpenGL
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import math

temporalActual = 0
cuadruplo_actual = 0

dirproc = []
memGlobal = []
memActiva = []
memPasada = []
memNueva = []
memCtes = []
cuadruplos = []
pila = []
listaParamsMemActual = []
listaParamsMemNueva = []
funcionActual = 'main'
funcionPasada = ''
funcionNueva = ''
params = 0
existeRetorno = False
valorRetorno = None
value = None 
existeVerifica = False
existeVerificaDos = False

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
	if direccion>=1 and direccion<4000: #GLOBAL
		return memGlobal.set_valor_memoria(valor, direccion)
	if direccion>=4000 and direccion<8000: #LOCAL
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
	if op == 'SQUARE':
		return square
	if op == 'CIRCLE':
		return circle
	if op == 'TRIANGLE':
		return triangle
	if op == 'PRINT':
		return imprime
	if op == 'VERIFICA':
		return verifica

'''
=========================================================

Corregir el valor que va a asignar, puede ser booleano, 
cambiar el float

=========================================================
'''
def asignacion(c1, c2, c3):
	global existeRetorno
	global valorRetorno
	global value
	if existeRetorno == True:
		existeRetorno = False
		setValue(valorRetorno, c3)
	else:
		m = str(c3)
		if m[0] == '(':
			l = len(c3)
			m = int(c3[1:l-1])
			print  "M", getValue(m)

			if (c1>=1 and c1<1000) or (c1>=4000 and c1<5000) or (c1>=8000 and c1<9000) or (c1>=12000 and c1<13000):
				value = int(getValue(c1))
			if (c1>=1000 and c1<2000) or (c1>=5000 and c1<6000) or (c1>=9000 and c1<10000) or (c1>=13000 and c1<14000):
				value = float(getValue(c1))
			if (c1>=2000 and c1<3000) or (c1>=6000 and c1<7000) or (c1>=10000 and c1<11000) or (c1>=14000 and c1<15000):
				x = str(getValue(c1))
				if x == 'true':
					value = True
				elif x == 'false':
					value = False
				else:
					sys.exit()
			if (c1>=3000 and c1<4000) or (c1>=7000 and c1<8000) or (c1>=11000 and c1<12000) or (c1>=15000 and c1<16000):
				value = str(getValue(c1))

			setValue(value, getValue(m))

		else:

			if (c1>=1 and c1<1000) or (c1>=4000 and c1<5000) or (c1>=8000 and c1<9000) or (c1>=12000 and c1<13000):
				value = int(getValue(c1))
			if (c1>=1000 and c1<2000) or (c1>=5000 and c1<6000) or (c1>=9000 and c1<10000) or (c1>=13000 and c1<14000):
				value = float(getValue(c1))
			if (c1>=2000 and c1<3000) or (c1>=6000 and c1<7000) or (c1>=10000 and c1<11000) or (c1>=14000 and c1<15000):
				x = str(getValue(c1))
				if x == 'true':
					value = True
				elif x == 'false':
					value = False
				else:
					sys.exit()

			if (c1>=3000 and c1<4000) or (c1>=7000 and c1<8000) or (c1>=11000 and c1<12000) or (c1>=15000 and c1<16000):
				value = str(getValue(c1))

			setValue(value, c3)
			print getValue(c3)

		print "asign"	
		print getValue(getValue(m))


def suma(c1, c2, c3):
	global value
	global existeVerifica
	global existeVerificaDos

	if existeVerifica:
		existeVerifica = False
		existeVerificaDos = True
		value = int(getValue(c1)) + int(getValue(c2))
		setValue(value, c3)
	elif existeVerificaDos:
		existeVerificaDos = False
		value = int(getValue(c1)) + int(c2)
		setValue(value, c3)

		print "Aqui"
		print getValue(c1)
		print c2
		print getValue(c3)
	# Operacion normal de suma 
	else:
		# En caso de que sea una matriz
		m1 = str(c1)
		m2 = str(c2)
		if m1[0] == '(':
			l = len(c1)
			m1 = int(c1[1:l-1])
			c1 = getValue(m1)
		if m2[0] == '(':
			l = len(c2)
			m2 = int(c2[1:l-1])
			c2 = getValue(m2)

		value = float(getValue(c1)) + float(getValue(c2))
		setValue(value, c3)



def resta(c1, c2, c3):
	global value
	m1 = str(c1)
	m2 = str(c2)
	if m1[0] == '(':
		l = len(c1)
		m1 = int(c1[1:l-1])
		c1 = getValue(m1)
	if m2[0] == '(':
		l = len(c2)
		m2 = int(c2[1:l-1])
		c2 = getValue(m2)

	value = float(getValue(c1)) - float(getValue(c2))
	setValue(value, c3)
	

def multiplicacion(c1, c2, c3):
	global value
	global existeVerifica

	if existeVerifica:
		existeVerifica = False
		value = float(getValue(c1)) * float(c2)
		print getValue(c3)
	else:
		m1 = str(c1)
		m2 = str(c2)
		if m1[0] == '(':
			l = len(c1)
			m1 = int(c1[1:l-1])
			c1 = getValue(m1)
		if m2[0] == '(':
			l = len(c2)
			m2 = int(c2[1:l-1])
			c2 = getValue(m2)
		value = float(getValue(c1)) * float(getValue(c2))
	
	setValue(value, c3)



def division(c1, c2, c3):
	global value
	m1 = str(c1)
	m2 = str(c2)
	if m1[0] == '(':
		l = len(c1)
		m1 = int(c1[1:l-1])
		c1 = getValue(m1)
	if m2[0] == '(':
		l = len(c2)
		m2 = int(c2[1:l-1])
		c2 = getValue(m2)

	value = float(getValue(c1)) / float(getValue(c2))
	setValue(value, c3)

def greater_than(c1, c2, c3):
	global value
	m1 = str(c1)
	m2 = str(c2)
	if m1[0] == '(':
		l = len(c1)
		m1 = int(c1[1:l-1])
		c1 = getValue(m1)
	if m2[0] == '(':
		l = len(c2)
		m2 = int(c2[1:l-1])
		c2 = getValue(m2)

	value = float(getValue(c1)) > float(getValue(c2))
	setValue(value, c3)

def less_than(c1, c2, c3):
	global value
	m1 = str(c1)
	m2 = str(c2)
	if m1[0] == '(':
		l = len(c1)
		m1 = int(c1[1:l-1])
		c1 = getValue(m1)
	if m2[0] == '(':
		l = len(c2)
		m2 = int(c2[1:l-1])
		c2 = getValue(m2)

	value = float(getValue(c1)) < float(getValue(c2))
	setValue(value, c3)

def different(c1, c2, c3):
	global value
	m1 = str(c1)
	m2 = str(c2)
	if m1[0] == '(':
		l = len(c1)
		m1 = int(c1[1:l-1])
		c1 = getValue(m1)
	if m2[0] == '(':
		l = len(c2)
		m2 = int(c2[1:l-1])
		c2 = getValue(m2)

	value = float(getValue(c1)) != float(getValue(c2))
	setValue(value, c3)

def equal(c1, c2, c3):
	global value
	m1 = str(c1)
	m2 = str(c2)
	if m1[0] == '(':
		l = len(c1)
		m1 = int(c1[1:l-1])
		c1 = getValue(m1)
	if m2[0] == '(':
		l = len(c2)
		m2 = int(c2[1:l-1])
		c2 = getValue(m2)
	if ((c1>=2000 and c1<3000) or (c1>=6000 and c1<7000) or (c1>=10000 and c1<11000) or (c1>=14000 and c1<15000) and ((c2>=2000 and c2<3000) or (c2>=6000 and c2<7000) or (c2>=10000 and c2<11000) or (c2>=14000 and c2<15000))):
		value = getValue(c1) == getValue(c2)
		setValue(value, c3)
	else:
		value = float(getValue(c1)) == float(getValue(c2))
		setValue(value, c3)

def greater_equal_than(c1, c2, c3):
	global value
	m1 = str(c1)
	m2 = str(c2)
	if m1[0] == '(':
		l = len(c1)
		m1 = int(c1[1:l-1])
		c1 = getValue(m1)
	if m2[0] == '(':
		l = len(c2)
		m2 = int(c2[1:l-1])
		c2 = getValue(m2)

	value = float(getValue(c1)) >= float(getValue(c2))
	setValue(value, c3)

def less_equal_than(c1, c2, c3):
	global value
	m1 = str(c1)
	m2 = str(c2)
	if m1[0] == '(':
		l = len(c1)
		m1 = int(c1[1:l-1])
		c1 = getValue(m1)
	if m2[0] == '(':
		l = len(c2)
		m2 = int(c2[1:l-1])
		c2 = getValue(m2)

	value = float(getValue(c1)) <= float(getValue(c2))
	setValue(value, c3)

def gotof(c1, c2, c3):
	global value
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
	global memNueva
	global funcionNueva

	params = 0
	memNueva = Memoria(dirproc[c2]['Tamano']['ints'],dirproc[c2]['Tamano']['floats'],dirproc[c2]['Tamano']['strings'],dirproc[c2]['Tamano']['bools'],dirproc[c2]['Tamano']['tempInts'],dirproc[c2]['Tamano']['tempFloats'], dirproc[c2]['Tamano']['tempStrings'], dirproc[c2]['Tamano']['tempBools'])
	funcionNueva = c2

def param(c1, c2, c3):
	global params
	global listaParamsMemActual
	global listaParamsMemNueva

	listaParamsMemActual.append(getValue(c1))
	listaParamsMemNueva.append(c3)

	params = params + 1

	print listaParamsMemActual
	print listaParamsMemNueva

def gosub(c1, c2, c3):
	global params
	global cuadruplo_actual
	global pila
	global memPasada
	global funcionActual
	global dirproc
	global memActiva
	global memNueva
	global funcionNueva
	global listaParamsMemNueva

	if params == len(dirproc[c1]['OrderedParams']):
		pila.append([cuadruplo_actual, funcionActual, memActiva])
		memActiva  = memNueva
		funcionActual = funcionNueva
		
		cuadruplo_actual = c3

		i = 0
		while i < params:
			direccion = listaParamsMemNueva.pop()

			if direccion>=1 and direccion<4000: #GLOBAL
				return memGlobal.set_valor_memoria(listaParamsMemActual.pop(), direccion)
			if direccion>=4000 and direccion<8000: #LOCAL
				return memActiva.set_valor_memoria(listaParamsMemActual.pop(), direccion)
			if direccion>=8000 and direccion<12000: #TEMPORAL
				return memActiva.set_valor_memoria(listaParamsMemActual.pop(), direccion)
			if direccion>=12000 and direccion<16000: #CONSTANTE
				return memCtes.set_valor_memoria(listaParamsMemActual.pop(), direccion)

			i = i + 1

		params = 0

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
	valorRetorno = getValue(c3)

def verifica(c1, c2, c3):
	global value
	global existeVerifica

	existeVerifica = True
	value = int(getValue(c1))

	if not (value>=c2 and value<=c3):
		print 'Array overflow'
		sys.exit()






'''
============================================
FUNCIONES ESPECIALES OpenGL
============================================
'''

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

def square(c1, c2, c3):
	x1 = float(getValue(c1[0]))
	y1 = float(getValue(c1[1]))
	size = float(getValue(c1[2]))

	glColor3ub(255, 0, 0)
	glTranslated(x1, y1, 0)
	glScalef(size, size, 0)
	
	glBegin(GL_POLYGON)
	glVertex3f(1.0, 1.0, 0.0)
	glVertex3f(-1.0, 1.0, 0.0)
	glVertex3f(-1.0, -1.0, 0.0)
	glVertex3f(1.0, -1.0, 0.0)
	glEnd()

def circle(c1, c2, c3):
	x = float(getValue(c1[0]))
	y = float(getValue(c1[1]))
	radio = float(getValue(c1[2]))

	glColor3ub(255, 0, 0)
	glTranslated(x, y, 0)
	#glScalef(size, size, 0)

	glBegin(GL_LINE_LOOP)
	for i in range(100):
		glVertex2f(x + (radio * math.cos(i * (2 * math.pi) / 100)), y + (radio * math.sin(i * (2 * math.pi) / 100)))
	glEnd()

def triangle(c1, c2, c3):
	x = float(getValue(c1[0]))
	y = float(getValue(c1[1]))
	tam = float(getValue(c1[2]))

	glColor3ub(255, 0, 0)
	glTranslated(x, y, 0)
	glScalef(tam, tam, 0)

	glBegin(GL_TRIANGLES)
	glVertex3f(0.5, 0, 0)
	glVertex3f(-0.5, 0, 0)
	glVertex3f(0, 1, 0)
	glEnd()

def imprime(c1, c2, c3):
	m = str(c3)
	if m[0] == '(':
		l = len(c3)
		m = int(c3[1:l-1])
		print getValue(getValue(m))
	else:
		print getValue(c3)

def myKeyboard(key, x, y):
	if key == 'q':
		sys.exit()

window = 0                                             # glut window number
width, height = 500, 500   

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

		if currentCuad.op == '+'  or currentCuad.op == '=' or currentCuad.op == '*' or currentCuad.op == '-' or currentCuad.op == '/' or currentCuad.op == '>' or currentCuad.op == '<' or currentCuad.op == '<>' or currentCuad.op == '==' or currentCuad.op == '>=' or currentCuad.op == '<=' or currentCuad.op == 'GOTOF' or currentCuad.op == 'GOTO'  or currentCuad.op == 'ERA'  or currentCuad.op == 'GOSUB' or currentCuad.op == 'PARAM' or currentCuad.op == 'RET' or currentCuad.op == 'RETURN' or currentCuad.op == 'LINE' or currentCuad.op == 'SQUARE' or currentCuad.op == 'CIRCLE' or currentCuad.op == 'TRIANGLE' or currentCuad.op == 'PRINT' or currentCuad.op == 'VERIFICA':
			metodo = getMetodo(currentCuad.op)
			metodo(currentCuad.opdoIzq, currentCuad.opdoDer, currentCuad.res)
		

	glutKeyboardFunc(myKeyboard)
	glutDisplayFunc(draw)
	glutIdleFunc(draw)
	glutMainLoop()



	
	exit(-1)


