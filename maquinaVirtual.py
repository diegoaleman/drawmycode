from structs import *
from dmcparser import *
from cuadruplos import *
from Memoria import *
from copy import deepcopy
import OpenGL
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
from random import randint
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

fill = False
posXPrint = -450
posYPrint = 400


'''
=============================================================
	La funcion es llamada por parte del dmcparser y 
	trae como parametro el directorio de procesos,
	la memoria global, la memoria local, la memoria de
	constantes y todos los cuadruplos
=============================================================
'''
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


'''
=============================================================
	La funcion es llamada para obtener el valor real 
	que guarda una direccion. 
=============================================================
'''
def getValue(direccion):
	m = str(direccion)
	if m[0] == '(':
		l1 = len(direccion)
		m = int(direccion[1:l1-1])
		direccion = m
	if direccion>=1 and direccion<4000: #LOCAL
		return memGlobal.get_valor_memoria(direccion)
	elif direccion>=4000 and direccion<8000: #GLOBAL
		return memActiva.get_valor_memoria(direccion)
	elif direccion>=8000 and direccion<12000: #TEMPORAL
		return memActiva.get_valor_memoria(direccion)
	elif direccion>=12000 and direccion<16000: #CONSTANTE
		return memCtes.get_valor_memoria(direccion)
	else:
		print 'Error. Direccion de memoria invalida'
		sys.exit()



'''
=============================================================
	La funcion es llamada para guardar en una direccion 
	de memoria dada un valor
=============================================================
'''
def setValue(valor, direccion):
	if direccion>=1 and direccion<4000: #GLOBAL
		return memGlobal.set_valor_memoria(valor, direccion)
	elif direccion>=4000 and direccion<8000: #LOCAL
		return memActiva.set_valor_memoria(valor, direccion)
	elif direccion>=8000 and direccion<12000: #TEMPORAL
		return memActiva.set_valor_memoria(valor, direccion)
	elif direccion>=12000 and direccion<16000: #CONSTANTE
		return memCtes.set_valor_memoria(valor, direccion)
	else:
		print 'Error. Direccion de memoria invalida'
		sys.exit()



'''
=============================================================
	Regresa la funcion accion que debe de ser ejecutada
	tomando como parametro el primer elemento, el 
	operador, del cuadruplo
=============================================================
'''
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
	if op == 'ARC':
		return arc
	if op == 'PRINT':
		return imprime
	if op == 'VERIFICA':
		return verifica
	if op == 'LINEWIDTH':
		return linewidth
	if op == 'LINECOLOR':
		return linecolor
	if op == 'STARTFILL':
		return startfill
	if op == 'STOPFILL':
		return stopfill
	if op == 'RANDOM':
		return random
	if op == 'STAR':
		return star


'''
=============================================================
	Es llamado para asignar a la direccion c3 el valor 
	guardado en la direccion c1
=============================================================
'''
def asignacion(c1, c2, c3):
	global existeRetorno
	global valorRetorno
	global value
	if existeRetorno == True:
		existeRetorno = False
		setValue(valorRetorno, c3)
	else:
		m1 = str(c1)
		if m1[0] == '(':
			l1 = len(c1)
			m1 = int(c1[1:l1-1])
			c1 = getValue(m1)

		m = str(c3)
		if m[0] == '(':
			l = len(c3)
			m = int(c3[1:l-1])

			if (c1>=1 and c1<1000) or (c1>=4000 and c1<5000) or (c1>=8000 and c1<9000) or (c1>=12000 and c1<13000):
				value = int(getValue(c1))
			elif (c1>=1000 and c1<2000) or (c1>=5000 and c1<6000) or (c1>=9000 and c1<10000) or (c1>=13000 and c1<14000):
				value = float(getValue(c1))
			elif (c1>=2000 and c1<3000) or (c1>=6000 and c1<7000) or (c1>=10000 and c1<11000) or (c1>=14000 and c1<15000):
				x = str(getValue(c1))
				if x == 'True':
					value = True
				elif x == 'False':
					value = False
				else:
					sys.exit()
			elif (c1>=3000 and c1<4000) or (c1>=7000 and c1<8000) or (c1>=11000 and c1<12000) or (c1>=15000 and c1<16000):
				value = str(getValue(c1))
			else:
				print 'Error. Direccion de memoria invalida'
				sys.exit()

			setValue(value, getValue(m))

			#print "asign"	
			#print getValue(getValue(m))

		else:

			if (c1>=1 and c1<1000) or (c1>=4000 and c1<5000) or (c1>=8000 and c1<9000) or (c1>=12000 and c1<13000):
				value = int(getValue(c1))
			elif (c1>=1000 and c1<2000) or (c1>=5000 and c1<6000) or (c1>=9000 and c1<10000) or (c1>=13000 and c1<14000):
				value = float(getValue(c1))
			elif (c1>=2000 and c1<3000) or (c1>=6000 and c1<7000) or (c1>=10000 and c1<11000) or (c1>=14000 and c1<15000):
				x = str(getValue(c1))
				if x == 'True':
					value = True
				elif x == 'False':
					value = False
				else:
					sys.exit()
			elif (c1>=3000 and c1<4000) or (c1>=7000 and c1<8000) or (c1>=11000 and c1<12000) or (c1>=15000 and c1<16000):
				value = str(getValue(c1))
			else:
				print 'Error. Direccion de memoria invalida'
				sys.exit()

			setValue(value, c3)




'''
=============================================================
	Suma los valores que se encuentran en la direccion c1 
	y c2 y los guarda en la direccion temporal c3
=============================================================
'''
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

		#print "Aqui"
		#print getValue(c1)
		#print c2
		#print getValue(c3)
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



'''
=============================================================
	Resta los valores que se encuentran en la direccion c1 
	y c2 y los guarda en la direccion temporal c3
=============================================================
'''
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
	



'''
=============================================================
	Multiplica los valores que se encuentran en la direccion c1 
	y c2 y los guarda en la direccion temporal c3
=============================================================
'''
def multiplicacion(c1, c2, c3):
	global value
	global existeVerifica

	if existeVerifica:
		existeVerifica = False
		value = float(getValue(c1)) * float(c2)
		#print getValue(c3)
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




'''
=============================================================
	Divide los valores que se encuentran en la direccion c1 
	y c2 y los guarda en la direccion temporal c3
=============================================================
'''
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




'''
=============================================================
	Compara con mayor que a los valores que se encuentran 
	en la direccion c1 y c2 y los guarda en la direccion 
	temporal c3
=============================================================
'''
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





'''
=============================================================
	Compara con menor que a los valores que se encuentran 
	en la direccion c1 y c2 y los guarda en la direccion 
	temporal c3
=============================================================
'''
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






'''
=============================================================
	Compara con mayor que a los valores que se encuentran 
	en la direccion c1 y c2 y los guarda en la direccion 
	temporal c3
=============================================================
'''
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






'''
=============================================================
	Compara con igualdad a los valores que se encuentran 
	en la direccion c1 y c2 y los guarda en la direccion 
	temporal c3
=============================================================
'''
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
		x = str(getValue(c2))
		if x == 'True':
			c2 = True
		elif x == 'False':
			c2 = False
		else:
			sys.exit()
		value = getValue(c1) == c2
		setValue(value, c3)
	else:
		value = float(getValue(c1)) == float(getValue(c2))
		setValue(value, c3)





'''
=============================================================
	Compara con mayor igual a los valores que se encuentran 
	en la direccion c1 y c2 y los guarda en la direccion 
	temporal c3
=============================================================
'''
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






'''
=============================================================
	Compara con menor igual a los valores que se encuentran 
	en la direccion c1 y c2 y los guarda en la direccion 
	temporal c3
=============================================================
'''
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





'''
=============================================================
	Al ser llamada la funcion revisa el valor que tiene 
	en la direccion c1, en caso de ser falso salta a la
	posicion que contiene c3, en caso de ser verdadera c1
	sigue al sigueinte cuadruplo
=============================================================
'''
def gotof(c1, c2, c3):
	global value
	global cuadruplo_actual
	value = getValue(c1)
	if value == False:
		cuadruplo_actual = c3


'''
=============================================================
	Al ser llamada la funcion salta al cuadruplo que se
	encuentra en c3
=============================================================
'''
def goto(c1, c2, c3):
	global cuadruplo_actual
	cuadruplo_actual = c3



'''
=============================================================
	Al ser llamado, el era nos indica que se debe de ir 
	preparando ya que pronto se llamara a otra funcion
=============================================================
'''
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



'''
=============================================================
	Al ser llamado el param nos indica que se debe de 
	guardar el valor en la direccion c1 en la direccion 
	c3. Pero la direccion c1 es de la memoria que va a
	estar pronto en la pila y la direccion de c3 es de la
	memoria de la nueva funcion, que acaba de ser cargada 
	en era
=============================================================
'''
def param(c1, c2, c3):
	global params
	global listaParamsMemActual
	global listaParamsMemNueva

	listaParamsMemActual.append(getValue(c1))
	listaParamsMemNueva.append(c3)

	params = params + 1

	#print listaParamsMemActual
	#print listaParamsMemNueva



'''
=============================================================
	Esta funcion es llamada cuando previamente se llamo 
	al era y posiblemente param. En esta ya se hace el 
	cambio de memoria y se cambia el cuadruplo actual
	al inicio de la funcion llamada
=============================================================
'''
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
			elif direccion>=4000 and direccion<8000: #LOCAL
				return memActiva.set_valor_memoria(listaParamsMemActual.pop(), direccion)
			elif direccion>=8000 and direccion<12000: #TEMPORAL
				return memActiva.set_valor_memoria(listaParamsMemActual.pop(), direccion)
			elif direccion>=12000 and direccion<16000: #CONSTANTE
				return memCtes.set_valor_memoria(listaParamsMemActual.pop(), direccion)
			else:
				print 'Error. Direccion de memoria invalida'
				sys.exit()

			i = i + 1

		params = 0

	else:
		print 'Numero incorrecto de parametros en funcion'
		sys.exit()


'''
=============================================================
	Esta funcion es colocada al finalizar la funcion y 
	se utiliza para regresar a la funcion que la llamo
=============================================================
'''
def ret(c1, c2, c3):
	global memActiva
	global cuadruplo_actual
	global funcionActual
	
	p = pila.pop()
	memActiva = p[2]

	funcionActual = p[1]
	cuadruplo_actual = p[0]



'''
=============================================================
	Esta funcion se encarga de regresar a la funcion pasada
	el valor que debe de ser regresado por la actual
=============================================================
'''
def retorno(c1, c2, c3):
	global valorRetorno
	global existeRetorno

	existeRetorno = True
	valorRetorno = getValue(c3)



'''
=============================================================
	Esta funcion se encarga de verificar que el valor que
	tiene direccion c1 se encuentre entre el rango de c2 y c3
=============================================================
'''
def verifica(c1, c2, c3):
	global value
	global existeVerifica

	existeVerifica = True
	value = int(getValue(c1))

	if not (value>=c2 and value<=c3):
		print 'Index fuera de los limites'
		sys.exit()







'''
=============================================================
	Funcion especial que dibuja linea
=============================================================
'''
def line(c1, c2, c3):
	x1 = getValue(c1[0])
	y1 = getValue(c1[1])
	x2 = getValue(c1[2])
	y2 = getValue(c1[3])
	
	glBegin(GL_LINES);
	glVertex3f(float(x1), float(y1),0.0)
	glVertex3f(float(x2), float(y2),0.0)
	glEnd()


'''
=============================================================
	Funcion especial que dibuja un cuadrado
=============================================================
'''
def square(c1, c2, c3):
	x1 = float(getValue(c1[0]))
	y1 = float(getValue(c1[1]))
	size = float(getValue(c1[2]))

	glPushMatrix()
	glTranslated(x1, y1, 0)
	glScalef(size, size, 0)
	if not fill:
		glBegin(GL_LINE_LOOP)
		glVertex3f(1.0, 1.0, 0.0)
		glVertex3f(-1.0, 1.0, 0.0)
		glVertex3f(-1.0, -1.0, 0.0)
		glVertex3f(1.0, -1.0, 0.0)
		glEnd()
	else:
		glBegin(GL_POLYGON)
		glVertex3f(1.0, 1.0, 0.0)
		glVertex3f(-1.0, 1.0, 0.0)
		glVertex3f(-1.0, -1.0, 0.0)
		glVertex3f(1.0, -1.0, 0.0)
		glEnd()
	glPopMatrix()


'''
=============================================================
	Funcion especial que dibuja un circulo
=============================================================
'''
def circle(c1, c2, c3):
	x = float(getValue(c1[0]))
	y = float(getValue(c1[1]))
	radio = float(getValue(c1[2]))

	glPushMatrix()

	glTranslated(x, y, 0)
	#glScalef(size, size, 0)

	glBegin(GL_LINE_LOOP)
	for i in range(100):
		glVertex2f(x + (radio * math.cos(i * (2 * math.pi) / 100)), y + (radio * math.sin(i * (2 * math.pi) / 100)))
	glEnd()
	glPopMatrix()



'''
=============================================================
	Funcion especial que dibuja un triangulo
=============================================================
'''
def triangle(c1, c2, c3):
	x = float(getValue(c1[0]))
	y = float(getValue(c1[1]))
	tam = float(getValue(c1[2]))

	glPushMatrix()
	glTranslated(x, y, 0)
	glScalef(tam, tam, 0)

	glBegin(GL_TRIANGLES)
	glVertex3f(0.5, 0, 0)
	glVertex3f(-0.5, 0, 0)
	glVertex3f(0, 1, 0)
	glEnd()
	glPopMatrix()



'''
=============================================================
	Funcion especial que dibuja un arco
=============================================================
'''
def arc(c1, c2, c3):
	x1=float(getValue(c1[0]))
	y1=float(getValue(c1[1]))
	x2=float(getValue(c1[2]))
	y2=float(getValue(c1[3]))
	PI = 3.14
	step=5.0;
	glBegin(GL_LINE_STRIP)
	angle=x2
	while angle<=y2:
		rad  = PI*angle/180
		x  = x1+100*cos(rad)
		y  = y1+100*sin(rad)
		glVertex(x,y,0.0)
		angle+=step
	glEnd()



'''
=============================================================
	Funcion especial que dibuja el ancho de la linea 
	de la figura a ser dibujada
=============================================================
'''
def linewidth(c1, c2, c3):
	width = float(getValue(c1))
	glLineWidth(width)



'''
=============================================================
	Funcion especial que colorea la linea del color req
=============================================================
'''
def linecolor(c1, c2, c3):
	red = int(getValue(c1[0]))
	green = int(getValue(c1[1]))
	blue = int(getValue(c1[2]))
	glColor3ub(red,green,blue)



'''
=============================================================
	Rellena la figura del color indicado
=============================================================
'''
def startfill(c1, c2, c3):
	global fill
	red = int(getValue(c1[0]))
	green = int(getValue(c1[1]))
	blue = int(getValue(c1[2]))
	glColor3ub(red,green,blue)
	fill = True



'''
=============================================================
	Detiene el rellenado de la figura
=============================================================
'''
def stopfill(c1, c2, c3):
	global fill
	glColor3ub(0,0,0)
	fill = False



'''
=============================================================
	Regresa un valor random que se encuentre entre 
	los valores de c1 y c2 y lo guarda en la direccion c3
=============================================================
'''
def random(c1, c2, c3):
	global fill
	inf = int(getValue(c1))
	sup = int(getValue(c2))

	rand = randint(inf,sup)
	setValue(rand, c3)



'''
=============================================================
	Funcion especial que pinta una estrella 
=============================================================
'''
def star(c1, c2, c3):

	x = float(getValue(c1[0]))
	y = float(getValue(c1[1]))
	tam = float(getValue(c1[2]))

	glPushMatrix()
	glTranslated(x, y, 0)
	glScalef(tam, tam, 0)
	if fill:

		glBegin(GL_POLYGON)
		glVertex2f(x-10,  y+00)
		glVertex2f(x+10,  y+00)
		glVertex2f(x+00,  y-05)
		glEnd()
		glBegin(GL_POLYGON)
		glVertex2f(x+00,  y+7.5)
		glVertex2f(x+2.5, y-2.5)
		glVertex2f(x-05,  y-10)
		glEnd()
		glBegin(GL_POLYGON)
		glVertex2f(x+00,  y+7.5)
		glVertex2f(x+05,  y-10)
		glVertex2f(x-2.5, y-2.5)
		glEnd()
	else:
		glBegin(GL_LINE_LOOP)
		glVertex2f(x-10,  y+00)
		glVertex2f(x+10,  y+00)
		glVertex2f(x+00,  y-05)
		glEnd()
		glBegin(GL_LINE_LOOP)
		glVertex2f(x+00,  y+7.5)
		glVertex2f(x+2.5, y-2.5)
		glVertex2f(x-05,  y-10)
		glEnd()
		glBegin(GL_LINE_LOOP)
		glVertex2f(x+00,  y+7.5)
		glVertex2f(x+05,  y-10)
		glVertex2f(x-2.5, y-2.5)
		glEnd()
	glPopMatrix()



'''
=============================================================
	Imprime el valor el valor de c3 en c1 como x y c2 como y
=============================================================
'''
def imprime(c1, c2, c3):
	m = str(c3)
	if m[0] == '(':
		l = len(c3)
		m = int(c3[1:l-1])
		print getValue(getValue(m))
		printWindow(getValue(getValue(m)))
	else:
		print getValue(c3)
		printWindow(getValue(c3))

'''
=============================================================
	Funciones de OpenGl
=============================================================
'''
def myKeyboard(key, x, y):
	if key == 'q' or key == 'Q':
		sys.exit()

width, height = 500, 500   
def printWindow(output):
	global posYPrint
	global posXPrint
	output = str(output)
	glLineWidth(2)
	glColor3f(0.0, 0.0, 0.0)
	glPushMatrix()
	glTranslated(posXPrint,posYPrint,0)
	glScalef(0.3,0.3,0.0)
	for ch in output:
		glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(ch))
	glPopMatrix()
	if posYPrint > -400:
		posYPrint = posYPrint - 60
	else:
		posYPrint = 400;
		posXPrint = posXPrint + 100;

def refresh2d(width, height):
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glClearColor(1.0,1.0,1.0,1.0)
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(-width, width, -height, height, 0.0, 100.0)
	glMatrixMode (GL_MODELVIEW)
	glLoadIdentity()

def reshape(w, h):
    global width, height
    width = w
    height = h
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-width, width, -height, height, 0.0, 100.0)
    glMatrixMode (GL_MODELVIEW)
    
def draw():                         
	glutSwapBuffers() 




'''
=============================================================
	Este es el el main del juego, en esta funcion se 
	inicializa opengl y su pantalla. Tambien se traversa
	por cada uno de los cuadruplos con un for y se panda
	a llamar la accion dependiendo a su respectivo op
=============================================================
'''
def main():
	global cuadruplo_actual
	glutInit(sys.argv)
	glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB)
	glutInitWindowSize (500, 500)
	glutInitWindowPosition (100, 100)
	glutCreateWindow ('DRAWMYCODE')
	glClearColor(1.0,1.0,1.0,1.0)
	glColor3ub(0, 0, 0);
	refresh2d(width, height)                      
	

	cuadruplos_totales = len(cuadruplos)
	while cuadruplo_actual < cuadruplos_totales:
		currentCuad = cuadruplos[cuadruplo_actual]
		cuadruplo_actual =  cuadruplo_actual + 1

		#print currentCuad.op, currentCuad.opdoIzq, currentCuad.opdoDer, currentCuad.res

		if currentCuad.op == '+'  or currentCuad.op == '=' or currentCuad.op == '*' or currentCuad.op == '-' or currentCuad.op == '/' or currentCuad.op == '>' or currentCuad.op == '<' or currentCuad.op == '<>' or currentCuad.op == '==' or currentCuad.op == '>=' or currentCuad.op == '<=' or currentCuad.op == 'GOTOF' or currentCuad.op == 'GOTO'  or currentCuad.op == 'ERA'  or currentCuad.op == 'GOSUB' or currentCuad.op == 'PARAM' or currentCuad.op == 'RET' or currentCuad.op == 'RETURN' or currentCuad.op == 'LINE' or currentCuad.op == 'SQUARE' or currentCuad.op == 'CIRCLE' or currentCuad.op == 'TRIANGLE' or currentCuad.op == 'PRINT' or currentCuad.op == 'VERIFICA' or currentCuad.op == 'LINEWIDTH' or currentCuad.op == 'LINECOLOR' or currentCuad.op == 'STARTFILL' or currentCuad.op == 'STOPFILL' or currentCuad.op == 'RANDOM' or currentCuad.op == 'ARC' or currentCuad.op == 'STAR':
			metodo = getMetodo(currentCuad.op)
			metodo(currentCuad.opdoIzq, currentCuad.opdoDer, currentCuad.res)
			#glutSwapBuffers()

	glutKeyboardFunc(myKeyboard)
	glutDisplayFunc(draw)
	glutIdleFunc(draw)
	glutReshapeFunc(reshape)
	glutMainLoop()



	
	exit(-1)


