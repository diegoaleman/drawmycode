from structs import *
from cubosemantico import *
from tablas import *
from dmcparser import *
from maquinaVirtual import *
import sys

'''
	=======================================================
	pilaO -> Almacena la direccion de los operandos 
	pOper -> Almacena los operandos 
	pTipos -> Almacena los tipos de los operandos
	pSaltos -> Almacena los saltos de cuadruplos, 
			   utilizada en las condiciones, ciclos y para 
			   ir al cuadruplo inicialdel main
	=======================================================
'''
pilaO = Stack()
pOper = Stack()
pTipos = Stack()
pSaltos = Stack()
pDimensionada = Stack()

cuadruplos = [] # Lista que almacena la lista de cuadruplos


contSaltos = 0  # Contador de saltos que indica el numero del cuadruplo actual 
actualAccessDIM = 1 # Dimension actual de la matriz a la que se esta accesando
actualAccessMatrix = {} # Diccionario que contiene la descripcion de la matriz a la que actualmente se esta accesando
actualIDDim = None # Guarda el nombre de la variable dimensionada
actualDirBaseMatrix = None # Guarda la direccion base de la matriz actual

'''
	===========================================================================
	La clase Cuadruplo se utiliza para crear objetos que representan los 
	cuadruplos generados para luego ser almacenados en una lista de objetos.
	El atributo 'op' guarda el operador del cuadruplo
	El atributo 'opdoIzq' guarda el operando izquierdo del cuadruplo
	El atributo 'opdoDer' guarda el operando derecho del cuadruplo
	El atributo 'res' guarda el resultado de la operacion del cuadruplo
	===========================================================================
'''
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
	===========================================================
	Genera cuadruplo GOTO al main y espera cuadruplo de inicio 
	del main
	===========================================================
'''
def goto_main_quad():
	global pSaltos
	genera_cuadruplo = Cuadruplo("GOTO","","","")
	push_cuadruplo(genera_cuadruplo)
	pSaltos.push(0);

'''
	===========================================================
	Regresa el numero del cuadruplo en donde inicia el main
	===========================================================
'''
def iniciaMain():
	global pSaltos
	inicioMain = pSaltos.pop()
	cuadruplos[inicioMain].res = contSaltos

''' 
	============================================
	Meter direccion y tipo del ID en pilaO
	============================================
''' 
def exp_1(dirvar,tipo):
	global pilaO
	global pTipos

	pilaO.push(dirvar)
	pTipos.push(tipo)


''' 
	============================================
	Si encuentra operador * o /, lo mete en pOper
	============================================
'''
def exp_2(product_division):
	global pOper
	pOper.push(product_division)


''' 
	============================================
	Si encuentra operador + o -, lo mete en pOper
	============================================
'''
def exp_3(plus_minus):
	global pOper
	pOper.push(plus_minus)


''' 
	============================================
	Si top(pOper) == '*' o '/'
	============================================
'''
def exp_4():
	global pOper
	global pTipos
	global pilaO

	if not pOper.isEmpty():
		if pOper.peek() == '*' or pOper.peek() == '/':
			op = pOper.pop()

			opdoDer = pilaO.pop()
			tipoDer = pTipos.pop()
			
			opdoIzq = pilaO.pop()
			tipoIzq = pTipos.pop()

			tipoRes = cuboSemantico[tipoIzq][tipoDer][op];

			if tipoRes != "Error":
				temp = set_dir_temp(tipoRes)			
				genera_cuadruplo = Cuadruplo(op,opdoIzq,opdoDer,temp)
				push_cuadruplo(genera_cuadruplo)

				pilaO.push(temp)
				pTipos.push(tipoRes)
			else:
				sys.exit("Error. Tipos Incompatibles.")

'''
	============================================
	Si top(pOper) == '+' o '-'
	============================================
'''
def exp_5():
	global pOper
	global pTipos
	global pilaO

	if not pOper.isEmpty():
		if pOper.peek() == '+' or pOper.peek() == '-':
			op = pOper.pop()

			opdoDer = pilaO.pop()
			tipoDer = pTipos.pop()
			
			opdoIzq = pilaO.pop()
			tipoIzq = pTipos.pop()

			tipoRes = cuboSemantico[tipoIzq][tipoDer][op];

			if tipoRes != "Error":
				temp = set_dir_temp(tipoRes)			
				genera_cuadruplo = Cuadruplo(op,opdoIzq,opdoDer,temp)
				push_cuadruplo(genera_cuadruplo)

				pilaO.push(temp)
				pTipos.push(tipoRes)
			else:
				sys.exit("Error. Tipos Incompatibles.")

'''
	=======================================================
	Meter Fondo Falso en pOper para el manejo de parentesis
	=======================================================
'''
def exp_6():
	global pOper
	pOper.push('[')

'''
	============================================
	Sacar Fondo Falso (parentesis)
	============================================
'''
def exp_7():
	global pOper
	pOper.pop()

'''
	============================================
	Si encuentra operador and/or, lo mete en pOper
	============================================
'''
def exp_8(and_or):
	global pOper
	pOper.push(and_or)


'''
	=====================================================
	Si top(pOper) es and o or , sacar and/or de pOper
	=====================================================
'''
def exp_9():
	global pOper
	global pTipos
	global pilaO
	
	#printPilas()
	if not pOper.isEmpty():
		if pOper.peek() == 'and' or pOper.peek() == 'or':
			op = pOper.pop()

			opdoDer = pilaO.pop()
			tipoDer = pTipos.pop()

			opdoIzq = pilaO.pop()
			tipoIzq = pTipos.pop()

			tipoRes = cuboSemantico[tipoIzq][tipoDer][op];

			if tipoRes != "Error":
				temp = set_dir_temp(tipoRes)
				genera_cuadruplo = Cuadruplo(op,opdoIzq,opdoDer,temp)
				push_cuadruplo(genera_cuadruplo)
				pTipos.push(tipoRes)
				pilaO.push(temp)
			else:
				sys.exit("Error. Tipos Incompatibles.")

'''
	======================================================================
	Si encuentra operador de comparacion, meter < <= > >= <> == en pOper
	======================================================================
'''
def exp_10(oper_logic):
	global pOper
	pOper.push(oper_logic)


'''
	=====================================================
	Si top(pOper) es < <= > >= <> == , sacar de pOper
	====================================================
'''
def exp_11():
	global pOper
	global pTipos
	global pilaO
	
	#printPilas()
	if not pOper.isEmpty():
		if pOper.peek() == '<' or pOper.peek() == '<=' or pOper.peek() == '>' or pOper.peek() == '>=' or pOper.peek() == '<>' or pOper.peek() == '==':
			op = pOper.pop()

			opdoDer = pilaO.pop()
			tipoDer = pTipos.pop()

			opdoIzq = pilaO.pop()
			tipoIzq = pTipos.pop()

			tipoRes = cuboSemantico[tipoIzq][tipoDer][op];

			if tipoRes != "Error":
				temp = set_dir_temp(tipoRes)
				genera_cuadruplo = Cuadruplo(op,opdoIzq,opdoDer,temp)
				push_cuadruplo(genera_cuadruplo)
				pTipos.push(tipoRes)
				pilaO.push(temp)
			else:
				sys.exit("Error. Tipos Incompatibles.")


'''
	======================================================
	Si encuentra operador de asignacion, meter = en pOper
	======================================================
'''
def exp_12(asignOper):
	global pOper
	pOper.push(asignOper)


'''
	============================================
	Si top(pOper) es = , sacar = de pOper
	============================================
'''
def exp_13():
	global pOper
	global pTipos
	global pilaO
	
	if not pOper.isEmpty():
		if pOper.peek() == '=':
			op = pOper.pop()

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
	============================================================
	Estatuto PRINT, imprime en consola la expresion o constante
	============================================================
'''
def estatuto_print():
	global pilaO
	global pTipos

	res = pilaO.pop()
	pTipos.pop()
	genera_cuadruplo = Cuadruplo("PRINT", "", "", res)
	push_cuadruplo(genera_cuadruplo)


'''
	=============================================================
	Estatuto IF , validacion semantica del tipo de la condicion
	Si condicion es diferente de bool, marca error semantico.
	Si es bool, genera cuadruplo GOTOF con la condicion y guarda
	salto en falso
	=============================================================
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
	================================================================
	Estatuto ELSE, genera cuadruplo GOTO, saca salto en falso y 
	rellena cuadruplo en falso. Guarda salto a fin de condicion
	================================================================
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
	=========================================================
	Estatuto ENDIF, rellena cuadruplo de fin de la condicion
	=========================================================
'''
def estatuto_endif():
	global pilaO
	global pTipos
	global cuadruplos
	global pSaltos
	fin = pSaltos.pop()
	cuadruplos[fin].res = contSaltos

'''
	=====================================================
	Estatuto WHILE 1, Guarda contador actual de saltos. 
	Indica que inicia el while.
	=====================================================
'''
def estatuto_while_1():
	global pSaltos

	pSaltos.push(contSaltos)

'''
	======================================================
	Estatuto WHILE 2, Valida la condicion del ciclo. 
	Si el tipo no es bool, marca error semantico. 
	Si es bool, genera GOTOF indicando el cuadruplo al 
	que se dirige cuando la condicion es falsa.
	======================================================
'''
def estatuto_while_2():
	global pilaO
	global pTipos
	global pSaltos

	auxTipo = pTipos.pop()
	if auxTipo != "bool":
		sys.exit("Error Semantico. Se requiere operacion booleana")
	else:
		res = pilaO.pop()
		genera_cuadruplo = Cuadruplo("GOTOF", res, "", "")
		push_cuadruplo(genera_cuadruplo)
	pSaltos.push(contSaltos-1)

'''
	============================================
	Estatuto WHILE 3,  Obtiene el cuadruplo al 
	que se tiene que regresar cuando la condicion 
	del while se cumple. 
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
	Regresa numero del cuadruplo en el que inicia una funcion
	=========================================================
'''
def altaInicioFunc():
	global contSaltos
	return contSaltos

'''
	=========================================================
	Genera Accion Retorno, indica cuando termina una funcion
	Calcula el tamano de la funcion
	=========================================================
'''
def generaAccionRetorno(funcActual):
	totalTempInts = get_Total_Temp_Int()
	totalTempFloats = get_Total_Temp_Float()
	totalTempBools = get_Total_Temp_Bool()
	totalTempStrings = get_Total_Temp_String()
	if (funcActual != 'main'):
		genera_cuadruplo = Cuadruplo("RET", "", "", "")
		push_cuadruplo(genera_cuadruplo)
	return {'totalTempInts' : totalTempInts,'totalTempFloats':totalTempFloats,'totalTempBools':totalTempBools,'totalTempStrings':totalTempStrings}

'''
	=========================================================
	Genera Accion End, indica el final del main
	=========================================================
'''
def generaAccionEndMain():
	genera_cuadruplo = Cuadruplo("END", "", "", "")
	push_cuadruplo(genera_cuadruplo)


'''
	=========================================================
	Estatuto Llamada Funcion 2, Generar cuadruplo ERA, calcula 
	el tamano de la funcion a llamar para trabajar en ella.
	=========================================================
'''
def estatuto_llamadafunc_2(funcLlamada, tamMemoriaLocalLlamadaFunc):
	genera_cuadruplo = Cuadruplo("ERA",tamMemoriaLocalLlamadaFunc,funcLlamada,"")
	push_cuadruplo(genera_cuadruplo)

'''
	============================================================
	Estatuto Llamada Funcion 3, Genera cuadruplo PARAM, verifica
	que el tipo del argumento y parametro coincidan
	============================================================
'''
def estatuto_llamadafunc_3(dirParamActual, tipoParamActual):
	global pilaO
	argumento = pilaO.pop()
	tipoArgumento = pTipos.pop()

	if (tipoArgumento == tipoParamActual):
		genera_cuadruplo = Cuadruplo("PARAM",argumento,"",dirParamActual)
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit('Error. Tipo de argumento y parametro no coinciden.')

'''
	==================================================================
	Estatuto Llamada Funcion 6, Generar GOSUB al cuadruplo inicial de
	la variable llamada. Si el tipo es diferente de 
	void, iguala el  valor de retorno a la direccion de la funcion.
	==================================================================
'''
def estatuto_llamadafunc_6(funcLlamada,quadInicioFuncLlamada,tipoFuncLlamada,dirFuncLlamada):
	global contSaltos
	global pilaO
	global pTipos

	genera_cuadruplo = Cuadruplo("GOSUB",funcLlamada,"",quadInicioFuncLlamada)
	push_cuadruplo(genera_cuadruplo)

	if (tipoFuncLlamada != 'void'):
		res = set_dir_temp(tipoFuncLlamada)
		genera_cuadruplo = Cuadruplo("=",dirFuncLlamada,"",res)
		push_cuadruplo(genera_cuadruplo)
		pilaO.push(res)
		pTipos.push(tipoFuncLlamada)
	

'''
	===================================================================
	Estatuto RETURN, Genera RETURN de la funcion actual con el 
	valor de retorno e indica el fin de la funcion (RET). Si la 
	funcion es void o no coincide el tipo de retorno con el de la 
	funcion, marca error de semantica.
	===================================================================
'''
def estatuto_return(funcActual, tipoFuncActual):
	global pilaO
	global pTipos

	tipoVarRetorno = pTipos.pop()
	tipoFunc = tipoFuncActual

	if (tipoFuncActual != 'void') and (tipoVarRetorno==tipoFunc):
		varRetorno = pilaO.pop()
		genera_cuadruplo = Cuadruplo("RETURN",funcActual,"",varRetorno)
		push_cuadruplo(genera_cuadruplo)
		genera_cuadruplo = Cuadruplo("RET","","","")
		push_cuadruplo(genera_cuadruplo)
	elif (tipoFuncActual=='void') or (tipoVarRetorno!=tipoFunc):
		sys.exit("Error. Tipo de valor retorno no coincide con tipo de la funcion.")

'''
	===================================================================
	Regresa la lista de los cuadruplos. Se usa para mandarsela a la 
	maquina virtual
	===================================================================
'''
def getCuadruplos():
	return cuadruplos

'''
	==================================================================
	Estatuto Variable Dimensionada 2, obtiene ID de la variable
	dimensionada, inicializa DIM = 1, push ID y DIM en pDimensionada
	para indicar en que matriz se encuentra y en que dimension. 
	Marca fondo falso por si hay anidamiento
	================================================================
'''
def acceso_dimvar_2(accessingMatrix):
	global pilaO
	global pDimensionada
	global pOper
	global actualAccessDIM
	global actualIDDim
	global actualAccessMatrix
	actualAccessMatrix = accessingMatrix;
	idDim = pilaO.pop()
	actualIDDim = idDim
	actualAccessDIM = 1
	pDimensionada.push([idDim,actualAccessDIM])
	pOper.push('[')

'''
	================================================================
	Estatuto Variable Dimensionada 3, Genera cuadruplo VERIFICA
	en el que revisa que el indice de la dimensioneste dentro 
	de los valores limites. Si se encuentra en la primera dimension
	genera cuadruplo para multiplicacion de s1 * m1. Si se encuentra
	en la segunda dimension, genera cuadruplo para s1 * m1 + s2
	===============================================================
'''
def acceso_dimvar_3():
	global pilaO
	global pTipos
	global actualDirBaseMatrix

	Li_DIM = actualAccessMatrix['Dim'][actualAccessDIM]['Li']
	Ls_DIM = actualAccessMatrix['Dim'][actualAccessDIM]['Ls']
	m_DIM = actualAccessMatrix['Dim'][actualAccessDIM]['m']
	actualDirBaseMatrix = actualAccessMatrix['Dir']
	genera_cuadruplo = Cuadruplo("VERIFICA",pilaO.peek(),Li_DIM,Ls_DIM)
	push_cuadruplo(genera_cuadruplo)
	if actualAccessDIM == 1: #Si siguiente dimension es diferente de nulo
		aux = pilaO.pop()
		pTipos.pop()
		temp = set_dir_temp('int')
		genera_cuadruplo = Cuadruplo("*",aux,m_DIM,temp)
		push_cuadruplo(genera_cuadruplo)
		pilaO.push(temp)
	if actualAccessDIM == 2:
		aux2 = pilaO.pop()
		aux1 = pilaO.pop()
		pTipos.pop()
		temp = set_dir_temp('int')
		genera_cuadruplo = Cuadruplo("+",aux1,aux2,temp)
		push_cuadruplo(genera_cuadruplo)
		pilaO.push(temp)

'''
	================================================================
	Estatuto Variable Dimensionada 4, pasar a la siguiente dimension
	y actualizar la pila dimensionada
	================================================================
'''
def acceso_dimvar_4():
	global actualAccessDIM
	global pDimensionada

	actualAccessDIM = actualAccessDIM + 1
	pDimensionada.push([actualIDDim,actualAccessDIM])

'''
	================================================================
	Estatuto Variable Dimensionada 5, generar cuadruplo para
	calcular la direccion que se va a accesar dirBase + s1 * m1 + s2
	===============================================================
'''
def acceso_dimvar_5():
	global pilaO
	global pTipos
	global pOper
	global pDimensionada

	aux1 = pilaO.pop()
	temp = set_dir_temp('int')
	genera_cuadruplo = Cuadruplo("+",aux1,actualDirBaseMatrix,temp)
	push_cuadruplo(genera_cuadruplo)

	pilaO.push("("+ str(temp) + ")")
	pOper.pop()
	pDimensionada.pop()

'''
	============================================================
	Funcion integrada RANDOM, genera numero random entre valor
	limite inferior y superior
	============================================================
'''
def opfunc_random():
	global pilaO
	global pTipos
	superior = pilaO.pop()
	tipoSuperior = pTipos.pop()

	inferior = pilaO.pop()
	tipoInferior = pTipos.pop()

	temp = set_dir_temp('int')
	pilaO.push(temp)
	pTipos.push('int')
	genera_cuadruplo = Cuadruplo("RANDOM",inferior,superior,temp)
	push_cuadruplo(genera_cuadruplo)

'''
	============================================================
	Line Width, genera cuadruplo LINEWIDTH para indicar el ancho
	de la linea a dibujar.
	============================================================
'''
def dibujafunc_linewidth():
	global pilaO
	global pTipos

	width = pilaO.pop()
	tipoWidth = pTipos.pop()

	if (tipoWidth == 'int' or tipoWidth == 'float'):
		genera_cuadruplo = Cuadruplo("LINEWIDTH",width,"","")
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit("Error. Argumentos de funcion lineWidth deben ser numericos.")

'''
	============================================================
	Line Color, genera cuadruplo LINECOLOR que indica el RGB con
	el que se desea pintar la linea
	============================================================
'''
def dibujafunc_linecolor():
	global pilaO
	global pTipos

	blue = pilaO.pop()
	tipoBlue= pTipos.pop()

	green = pilaO.pop()
	tipoGreen = pTipos.pop()

	red = pilaO.pop()
	tipoRed = pTipos.pop()
	if tipoRed == 'int' and tipoGreen == 'int' and tipoBlue == 'int':
		genera_cuadruplo = Cuadruplo("LINECOLOR",[red,green,blue],"","")
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit("Error. Argumentos de funcion lineColor deben ser de tipo entero.")

'''
	=====================================================================
	Dibuja una linea en las coordenadas definidas, genera cuadruplo LINE
	=====================================================================
'''
def dibujafunc_line():
	global pilaO
	global pTipos

	cordY2 = pilaO.pop()
	tipoCordY2= pTipos.pop()

	cordX2 = pilaO.pop()
	tipoCordX2 = pTipos.pop()

	cordY1 = pilaO.pop()
	tipoCordY1 = pTipos.pop()

	cordX1 = pilaO.pop()
	tipoCordX1 = pTipos.pop()

	if (tipoCordX1 == 'int' or tipoCordX1 == 'float') and (tipoCordY1 == 'int' or tipoCordY1 == 'float') and (tipoCordX2 == 'int' or tipoCordX2 == 'float') and (tipoCordY2 == 'int' or tipoCordY2 == 'float'):
		genera_cuadruplo = Cuadruplo("LINE",[cordX1,cordY1,cordX2,cordY2],"","")
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit("Error. Argumentos de funcion line deben ser numericos.")
'''
	============================================================
	Dibuja un cuadrado en las coordenadas y con el tamano que se
	pasan como argumentos.
	Genera cuadruplo SQUARE
	============================================================
'''
def dibujafunc_square():
	global pilaO
	global pTipos

	tamano = pilaO.pop()
	tipoTamano= pTipos.pop()

	cordY= pilaO.pop()
	tipoCordY = pTipos.pop()

	cordX = pilaO.pop()
	tipoCordX = pTipos.pop()

	if (tipoTamano == 'int' or tipoTamano == 'float') and (tipoCordY == 'int' or tipoCordY == 'float') and (tipoCordX == 'int' or tipoCordX == 'float'):
		genera_cuadruplo = Cuadruplo("SQUARE",[cordX,cordY,tamano],"","")
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit("Error. Argumentos de funcion square deben ser numericos.")

'''
	============================================================
	Dibuja un circulo en las coordenadas y con el diametro que se
	pasan como argumentos.
	Genera cuadruplo CIRCLE
	============================================================
'''
def dibujafunc_circle():
	global pilaO
	global pTipos

	diametro = pilaO.pop()
	tipoDiametro = pTipos.pop()

	cordY= pilaO.pop()
	tipoCordY = pTipos.pop()

	cordX = pilaO.pop()
	tipoCordX = pTipos.pop()

	if (tipoDiametro == 'int' or tipoDiametro == 'float') and (tipoCordY == 'int' or tipoCordY == 'float') and (tipoCordX == 'int' or tipoCordX == 'float'):
		genera_cuadruplo = Cuadruplo("CIRCLE",[cordX,cordY,diametro],"","")
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit("Error. Argumentos de funcion circle deben ser numericos.")
'''
	============================================================
	Dibuja una estrella en las coordenadas y con el tamano que 
	se pasan como argumentos.
	Genera cuadruplo STAR
	============================================================
'''
def dibujafunc_star():
	global pilaO
	global pTipos

	tamano = pilaO.pop()
	tipoTamano= pTipos.pop()

	cordY= pilaO.pop()
	tipoCordY = pTipos.pop()

	cordX = pilaO.pop()
	tipoCordX = pTipos.pop()

	if (tipoTamano == 'int' or tipoTamano == 'float') and (tipoCordY == 'int' or tipoCordY == 'float') and (tipoCordX == 'int' or tipoCordX == 'float'):
		genera_cuadruplo = Cuadruplo("STAR",[cordX,cordY,tamano],"","")
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit("Error. Argumentos de funcion star deben ser numericos.")

'''
	============================================================
	Dibuja un triangulo en las coordenadas y con el tamano que 
	se pasan como argumentos.
	Genera cuadruplo TRIANGLE
	============================================================
'''
def dibujafunc_triangle():
	global pilaO
	global pTipos

	tamano = pilaO.pop()
	tipoTamano= pTipos.pop()

	cordY= pilaO.pop()
	tipoCordY = pTipos.pop()

	cordX = pilaO.pop()
	tipoCordX = pTipos.pop()

	if (tipoTamano == 'int' or tipoTamano == 'float') and (tipoCordY == 'int' or tipoCordY == 'float') and (tipoCordX == 'int' or tipoCordX == 'float'):
		genera_cuadruplo = Cuadruplo("TRIANGLE",[cordX,cordY,tamano],"","")
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit("Error. Argumentos de funcion triangle deben ser numericos.")
'''
	============================================================
	Dibuja un arco en las coordeanadas que se pasan como 
	argumentos.
	Genera cuadruplo ARC
	============================================================
'''
def dibujafunc_arc():
	global pilaO
	global pTipos

	cordY2 = pilaO.pop()
	tipoCordY2= pTipos.pop()

	cordX2 = pilaO.pop()
	tipoCordX2 = pTipos.pop()

	cordY1 = pilaO.pop()
	tipoCordY1 = pTipos.pop()

	cordX1 = pilaO.pop()
	tipoCordX1 = pTipos.pop()

	if (tipoCordX1 == 'int' or tipoCordX1 == 'float') and (tipoCordY1 == 'int' or tipoCordY1 == 'float') and (tipoCordX2 == 'int' or tipoCordX2 == 'float') and (tipoCordY2 == 'int' or tipoCordY2 == 'float'):
		genera_cuadruplo = Cuadruplo("ARC",[cordX1,cordY1,cordX2,cordY2],"","")
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit("Error. Argumentos de funcion arc deben ser numericos.")

'''
	============================================================
	Indice que comienza a rellenar figura con el valor RGB que 
	se pasa como parametro
	Genera cuadruplo STARTFILL
	============================================================
'''
def dibujafunc_startfill():
	global pilaO
	global pTipos

	blue = pilaO.pop()
	tipoBlue= pTipos.pop()

	green = pilaO.pop()
	tipoGreen = pTipos.pop()

	red = pilaO.pop()
	tipoRed = pTipos.pop()

	if tipoRed == 'int' and tipoGreen == 'int' and tipoBlue == 'int':
		genera_cuadruplo = Cuadruplo("STARTFILL",[red,green,blue],"","")
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit("Error. Argumentos de funcion startFill deben ser de tipo entero.")

'''
	============================================================
	Indica que termina de rellenar figura, reinicia valor RGB a
	blanco
	Genera cuadruplo STOPFILL
	============================================================
'''
def dibujafunc_stopfill():

	genera_cuadruplo = Cuadruplo("STOPFILL",255,255,255)
	push_cuadruplo(genera_cuadruplo)


'''
	============================================================
	Imprime las pilas
	============================================================
'''
def printPilas():
	print "pilaO ", pilaO.getElements()
	print "pTipos ", pTipos.getElements()
	print "pOper ", pOper.getElements()
	print "pSaltos ", pSaltos.getElements()
	print "pDimensionada" , pDimensionada.getElements()
	print_cuadruplos(cuadruplos)

'''
	============================================================
	Imprime los cuadruplos
	============================================================
'''
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
