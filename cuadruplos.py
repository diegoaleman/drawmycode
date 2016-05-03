from structs import *
from cubosemantico import *
from tablas import *
from dmcparser import *
from maquinaVirtual import *
import sys

pilaO = Stack()
pOper = Stack()
pTipos = Stack()
pSaltos = Stack()
pEjecucion = Stack()
pDimensionada = Stack()

# Inicia con el index 0
cuadruplos = []

# Inicia con el index 0
contSaltos = 0
actualAccessDIM = 1
actualAccessMatrix = {}
actualIDDim = None
actualDirBaseMatrix = None


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

def goto_main_quad():
	global pSaltos
	genera_cuadruplo = Cuadruplo("GOTO","","","")
	push_cuadruplo(genera_cuadruplo)
	pSaltos.push(0);

def iniciaMain():
	global pSaltos
	inicioMain = pSaltos.pop()
	cuadruplos[inicioMain].res = contSaltos
''' 
	============================================
	1. Meter direccion y tipo del ID en pilaO
	============================================
''' 
def exp_1(dirvar,tipo):
	global pilaO
	global pTipos

	pilaO.push(dirvar)
	pTipos.push(tipo)


''' 
	============================================
	2. Meter * o / en pOper
	============================================
'''
def exp_2(product_division):
	global pOper
	pOper.push(product_division)


''' 
	============================================
	3. Meter + o - en pOper
	============================================
'''
def exp_3(plus_minus):
	global pOper
	pOper.push(plus_minus)


''' 
	============================================
	4. Si top(pOper) == '*' o '/'
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
	5. Si top(pOper) == '+' o '-'
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
	============================================
	6. Meter Fondo Falso en pOper
	============================================
'''
def exp_6():
	global pOper
	pOper.push('[')

'''
	============================================
	7. Sacar Fondo Falso
	============================================
'''
def exp_7():
	global pOper
	pOper.pop()

'''
	============================================
	8. Meter AND/OR en pOper
	============================================
'''
def exp_8(and_or):
	global pOper
	pOper.push(and_or)


'''
	=====================================================
	9. Si top(pOper) es and o or , sacar and/or de pOper
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
	============================================
	10. Meter < <= > >= <> == en pOper
	============================================
'''
def exp_10(oper_logic):
	global pOper
	pOper.push(oper_logic)


'''
	=====================================================
	11. Si top(pOper) es < <= > >= <> == , sacar de pOper
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
	============================================
	12. Meter = en pOper
	============================================
'''
def exp_12(asignOper):
	global pOper
	pOper.push(asignOper)


'''
	============================================
	13. Si top(pOper) es = , sacar = de pOper
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
	============================================
	Estatuto PRINT
	============================================
'''
def estatuto_print():
	global pilaO
	global pTipos

	res = pilaO.pop()
	pTipos.pop()
	genera_cuadruplo = Cuadruplo("PRINT", "", "", res)
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
	=========================================================
	Genera Accion Retorno cuando termina una funcion
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
	Genera Accion End al final de MAIN
	=========================================================
'''
def generaAccionEndMain():
	genera_cuadruplo = Cuadruplo("END", "", "", "")
	push_cuadruplo(genera_cuadruplo)


'''
	=========================================================
	Estatuto Llamada Funcion 2
	=========================================================
'''
def estatuto_llamadafunc_2(funcLlamada, tamMemoriaLocalLlamadaFunc):
	genera_cuadruplo = Cuadruplo("ERA",tamMemoriaLocalLlamadaFunc,funcLlamada,"")
	push_cuadruplo(genera_cuadruplo)

'''
	=========================================================
	Estatuto Llamada Funcion 3
	=========================================================
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
	=========================================================
	Estatuto Llamada Funcion 6
	=========================================================
'''
def estatuto_llamadafunc_6(funcLlamada,quadInicioFuncLlamada,tipoFuncLlamada,dirFuncLlamada):
	global contSaltos
	global pEjecucion
	global pilaO
	global pTipos

	pEjecucion.push(contSaltos)
	genera_cuadruplo = Cuadruplo("GOSUB",funcLlamada,"",quadInicioFuncLlamada)
	push_cuadruplo(genera_cuadruplo)

	if (tipoFuncLlamada != 'void'):
		res = set_dir_temp(tipoFuncLlamada)
		genera_cuadruplo = Cuadruplo("=",dirFuncLlamada,"",res)
		push_cuadruplo(genera_cuadruplo)
		pilaO.push(res)
		pTipos.push(tipoFuncLlamada)
	


'''
	============================================
	Estatuto RETURN
	============================================
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
		sys.exit("Error. Tipo de variable retorno no coincide con tipo de la funcion.")

def getCuadruplos():
	return cuadruplos

'''
	============================================
	Estatuto Variable Dimensionada 2
	============================================
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
	============================================
	Estatuto Variable Dimensionada 3
	============================================
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
	============================================
	Estatuto Variable Dimensionada 4
	============================================
'''
def acceso_dimvar_4():
	global actualAccessDIM
	global pDimensionada

	actualAccessDIM = actualAccessDIM + 1
	pDimensionada.push([actualIDDim,actualAccessDIM])

'''
	============================================
	Estatuto Variable Dimensionada 5
	============================================
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
	============================================
	Funcion integrada RANDOM
	============================================
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
	============================================
	Line Width
	============================================
'''
def dibujafunc_linewidth():
	global pilaO
	global pTipos

	width = pilaO.pop()
	tipoWidth = pTipos.pop()

	genera_cuadruplo = Cuadruplo("LINEWIDTH",width,"","")
	push_cuadruplo(genera_cuadruplo)

'''
	============================================
	Line Color
	============================================
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
		sys.exit("Argumentos de funcion lineColor deben ser de tipo entero.")

'''
	============================================
	Dibuja una linea
	============================================
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

	if tipoCordX1 == 'int' and tipoCordY1 == 'int' and tipoCordX2 == 'int' and tipoCordY2 == 'int':
		genera_cuadruplo = Cuadruplo("LINE",[cordX1,cordY1,cordX2,cordY2],"","")
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit("Argumentos de funcion line deben ser de tipo entero.")
'''
	============================================
	Dibuja un cuadrado
	============================================
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

	if tipoTamano == 'int' and tipoCordY == 'int' and tipoCordX == 'int':
		genera_cuadruplo = Cuadruplo("SQUARE",[cordX,cordY,tamano],"","")
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit("Argumentos de funcion square deben ser de tipo entero.")

'''
	============================================
	Dibuja un circulo
	============================================
'''
def dibujafunc_circle():
	global pilaO
	global pTipos

	radio = pilaO.pop()
	tipoRadio = pTipos.pop()

	cordY= pilaO.pop()
	tipoCordY = pTipos.pop()

	cordX = pilaO.pop()
	tipoCordX = pTipos.pop()

	if tipoRadio == 'int' and tipoCordY == 'int' and tipoCordX == 'int':
		genera_cuadruplo = Cuadruplo("CIRCLE",[cordX,cordY,radio],"","")
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit("Argumentos de funcion circle deben ser de tipo entero.")
'''
	============================================
	Dibuja una estrella
	============================================
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

	if tipoTamano == 'int' and tipoCordY == 'int' and tipoCordX == 'int':
		genera_cuadruplo = Cuadruplo("STAR",[cordX,cordY,tamano],"","")
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit("Argumentos de funcion star deben ser de tipo entero.")

'''
	============================================
	Dibuja un triangulo
	============================================
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

	if tipoTamano == 'int' and tipoCordY == 'int' and tipoCordX == 'int':
		genera_cuadruplo = Cuadruplo("TRIANGLE",[cordX,cordY,tamano],"","")
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit("Argumentos de funcion triangle deben ser de tipo entero.")
'''
	============================================
	Dibuja un arco
	============================================
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

	if tipoCordX1 == 'int' and tipoCordY1 == 'int' and tipoCordX2 == 'int' and tipoCordY2 == 'int':
		genera_cuadruplo = Cuadruplo("ARC",[cordX1,cordY1,cordX2,cordY2],"","")
		push_cuadruplo(genera_cuadruplo)
	else:
		sys.exit("Argumentos de funcion arc deben ser de tipo entero.")

'''
	============================================
	Indice que comienza a rellenar figura
	============================================
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
		sys.exit("Argumentos de funcion startFill deben ser de tipo entero.")

'''
	============================================
	Indica que termina de rellenar figura
	============================================
'''
def dibujafunc_stopfill():

	genera_cuadruplo = Cuadruplo("STOPFILL",255,255,255)
	push_cuadruplo(genera_cuadruplo)


'''
	============================================
	Imprime las pilas
	============================================
'''
def printPilas():
	print "pilaO ", pilaO.getElements()
	print "pTipos ", pTipos.getElements()
	print "pOper ", pOper.getElements()
	print "pSaltos ", pSaltos.getElements()
	print "pDimensionada" , pDimensionada.getElements()
	print_cuadruplos(cuadruplos)

'''
	============================================
	Imprime los cuadruplos
	============================================
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
