# ------------------------------------------------------------
# Omar Antonio Carreon Medrano A01036074
# Diego Aleman A01139700
# dmcparser.py

# Run:
# python dmclex.py
# python dmcparser.py test/test1.txt

# *Change the test filename to test other files
# ------------------------------------------------------------


import ply.yacc as yacc
import sys
from tablas import *
from cuadruplos import *
from Memoria import *
from maquinaVirtual import *

# Get the token map from the lexer.
from dmclex import tokens
dirproc = {}
varsList = []
matrixList = []
paramsList = []
auxvars = {}
auxVarsDir = {}
varsGlobalesDir = {}
varsLocalesDir = {}

auxMatrixVarsDir = {}
auxMatrixVarsDir2 = {}
DIM = 1
R = 1
tablaConstantes = {}

nombrePrograma = None
scope = "Global"
nombreFunc = None
tipo = None
funcActual = None
funcGlobal = None
funcLlamada = None

matrixActual = None
# se usa para saber en que matriz estas leyendo en el bloque
varActual = None 

contTamFuncInt = 0
contTamFuncFloat = 0
contTamFuncBool = 0
contTamFuncString = 0
contNumLocales = 0
totalInts = 0
totalFloats = 0
totalBools = 0
totalStrings = 0

totalCtesInts = 0
totalCtesFloats = 0
totalCtesBools = 0
totalCtesStrings = 0

paramCounter = 0

def p_programa(p):
	'''programa : BEGIN PROGRAM goto_main_quad createDirProc ID altaPrograma SEMICOLON a LBRACKET crearGlobalTam b main RBRACKET SEMICOLON END'''
	p[0] = "Success"

def p_goto_main_quad(p):
	'''goto_main_quad :'''
	goto_main_quad()
def p_createDirProc(p):
	'''createDirProc :'''
	dirproc = {}

def p_altaPrograma(p):
	'''altaPrograma :'''
	global nombrePrograma
	global funcActual
	global funcGlobal
	global scope

	# Da de alta el programa en el DirProc
	nombre = p[-1]
	scope = "Global"
	nombrePrograma = nombre
	funcActual = nombrePrograma
	funcGlobal = nombrePrograma
	dirproc[nombrePrograma] = {}
	dirproc[nombrePrograma] = {'Tipo': 'programa', 'Vars': {}}

def p_crearGlobalTam(p):
	'''crearGlobalTam :'''
	global totalStrings
	global totalInts
	global totalFloats
	global totalBools

	dirproc[funcGlobal]['Tamano'] = {'ints' : totalInts, 'floats' : totalFloats, 'bools' : totalBools, 'strings' : totalStrings, 'tempInts' : 0, 'tempFloats' : 0, 'tempBools' : 0, 'tempStrings' : 0}

def p_a(p):
	'''a : vars
			|'''
	global varsGlobalesDir
	global auxVarsDir
	global varsList
	global auxMatrixVarsDir2
	global auxMatrixVarsDir
	# Copia solo las variables globales
	for elem in auxVarsDir:
		varsGlobalesDir[elem] = auxVarsDir[elem]
		varsGlobalesDir[elem]['Scope'] = 'Global'
		varsGlobalesDir[elem]['Tipo'] = auxVarsDir[elem]['Tipo']
		varsGlobalesDir[elem]['Valor'] = None
	dirproc[nombrePrograma]['Vars'] = varsGlobalesDir
	# Eliminar las variables que ya se guardaron como globales
	remove = [k for k in auxVarsDir]
	for k in remove: del auxVarsDir[k]

	# Copia solo las variables que son matrices
	for elem in auxMatrixVarsDir:
		varsGlobalesDir[elem] = auxMatrixVarsDir[elem]
		varsGlobalesDir[elem]['Scope'] = 'Global'
		varsGlobalesDir[elem]['Tipo'] = auxMatrixVarsDir[elem]['Tipo']
	dirproc[nombrePrograma]['Vars'] = varsGlobalesDir
	# Eliminar las variables que ya se guardaron como globales
	remove = [k for k in auxMatrixVarsDir]
	for k in remove: del auxMatrixVarsDir[k]

def p_vars(p):
	'''vars : VAR createGlobalTable c'''

def p_createGlobalTable(p):
	'''createGlobalTable :'''

def p_c(p):
	'''c : f SEMICOLON e'''
	
def p_f(p):
	'''f : d COLON tipo saveTipo
			| matrix'''	
	global varsList
	global auxVarsDir
	global scope 
	global totalStrings
	global totalInts
	global totalFloats
	global totalBools
	if len(p) == 5:
		while (len(varsList) > 0):
			# Le asigna una direccion a la variable de acuerdo a scope
			if scope == "Global":
				assignedDir = set_dir_global(tipo,1)
			elif scope == "Local":
				assignedDir = set_dir_local(tipo,1)
			
			if tipo == 'int':
				totalInts += 1
			elif tipo == 'float':
				totalFloats += 1
			elif tipo == 'string':
				totalStrings += 1
			elif tipo == 'bool':
				totalBools += 1
			# Guarda el tipo y direccion de la variable en el diccionario auxiliar de variables
			auxVarsDir[varsList.pop()] = {'Tipo' : tipo, 'Dir' : assignedDir}


def p_saveTipo(p):
	'''saveTipo :'''
	# Asigna el tipo a las variables 
	global tipo
	tipo = p[-1]

def p_d(p):
	'''d : ID saveVarID
			| ID saveVarID COMMA d'''

def p_saveVarID(p):
	'''saveVarID :'''
	# Guarda el nombre de las variables
	varsList.append(p[-1])
	
def p_tipo(p):
	'''tipo : INT
			| FLOAT
			| BOOL
			| STRING'''
	# Regresa el tipo de la variable
	p[0] = p[1]

def p_matrix(p):
	'''matrix :  mataux COLON INT'''


def p_mataux(p):
	'''mataux : ID saveMatrixID LSQUAREBRACKET CTEINT RSQUAREBRACKET LSQUAREBRACKET CTEINT RSQUAREBRACKET almacenaLimites
			| ID saveMatrixID LSQUAREBRACKET CTEINT RSQUAREBRACKET LSQUAREBRACKET CTEINT RSQUAREBRACKET almacenaLimites COMMA mataux'''
def p_saveMatrixID(p):
	'''saveMatrixID :'''
	global auxMatrixVarsDir
	global matrixActual
	global DIM
	global R 
	DIM = 1
	R = 1
	matrixActual = p[-1]
	auxMatrixVarsDir[p[-1]] = {'Tipo': 'int','Dim':{}}

def p_almacenaLimites(p):
	'''almacenaLimites :'''
	global auxMatrixVarsDir
	global auxMatrixVarsDir2
	global R
	global DIM
	global totalInts

	auxMatrixVarsDir[matrixActual]['Dim'] = {
			DIM: {
				'Li' : 0,
				'Ls' : int(p[-5]) - 1
			}
	}
	R = (int(auxMatrixVarsDir[matrixActual]['Dim'][DIM]['Ls']) - int(auxMatrixVarsDir[matrixActual]['Dim'][DIM]['Li']) + 1) * R
	DIM = DIM + 1

	auxMatrixVarsDir2 = {
			DIM: {
				'Li' : 0,
				'Ls' : int(p[-2]) - 1
			}
	}
	auxMatrixVarsDir[matrixActual]['Dim'].update(auxMatrixVarsDir2)
	R = (int(auxMatrixVarsDir[matrixActual]['Dim'][DIM]['Ls']) - int(auxMatrixVarsDir[matrixActual]['Dim'][DIM]['Li']) + 1) * R
	DIM = 1
	SUMA = 0
	AUX = R
	while (DIM <= len(auxMatrixVarsDir[matrixActual]['Dim'])):
		mDIM = R / ((int(auxMatrixVarsDir[matrixActual]['Dim'][DIM]['Ls']) - int(auxMatrixVarsDir[matrixActual]['Dim'][DIM]['Li']) + 1))
		R = mDIM
		SUMA = SUMA + int(auxMatrixVarsDir[matrixActual]['Dim'][DIM]['Li']) * mDIM
		auxMatrixVarsDir2 = {
			'm' : mDIM
		}
		auxMatrixVarsDir[matrixActual]['Dim'][DIM].update(auxMatrixVarsDir2)
		DIM = DIM + 1
	K = SUMA
	DIM = DIM - 1
	auxMatrixVarsDir2={
		'm' : K
	}
	auxMatrixVarsDir[matrixActual]['Dim'][DIM].update(auxMatrixVarsDir2)
	totalInts += AUX
	if scope == 'Global':
		auxMatrixVarsDir2={
			'Dir' : set_dir_global('int',AUX)
		}
	elif scope == 'Local':
		auxMatrixVarsDir2={
			'Dir' : set_dir_local('int',AUX)
		}
	auxMatrixVarsDir[matrixActual].update(auxMatrixVarsDir2)
def p_e(p):
	'''e : c 
			|'''

def p_b(p):
	'''b : funcion b
			|'''

def p_funcion(p):
	'''funcion : FUNC g ID altaFuncion LPARENTHESIS h RPARENTHESIS funcvars altaInicioFunc bloque SEMICOLON ENDFUNC accionRetorno'''

def p_accionRetorno(p):
	'''accionRetorno :'''
	global totalStrings
	global totalInts
	global totalFloats
	global totalBools
	totalTemps = generaAccionRetorno(funcActual)

	dirproc[funcActual]['Tamano'] = {'ints' : totalInts, 'floats' : totalFloats, 'bools' : totalBools, 'strings' : totalStrings, 'tempInts' : totalTemps['totalTempInts'], 'tempFloats' : totalTemps['totalTempFloats'], 'tempBools' : totalTemps['totalTempBools'], 'tempStrings' : totalTemps['totalTempStrings']}

	resetMemoriaLocal()


def p_funcvars(p):
	'''funcvars : vars
			|'''
	global varsList
	global auxVarsDir
	global varsLocalesDir
	global auxMatrixVarsDir
	global contTamFuncInt
	global contTamFuncFloat
	global contTamFuncBool
	global contTamFuncString
	global contNumLocales
	# Copia solo las variables locales
	for elem in auxVarsDir:
		varsLocalesDir[elem] = auxVarsDir[elem]
		varsLocalesDir[elem]['Scope'] = 'Local'
		varsLocalesDir[elem]['Tipo'] = auxVarsDir[elem]['Tipo']
	contNumLocales += len(auxVarsDir)
	dirproc[nombreFunc]['NumLocales'] = contNumLocales
	dirproc[nombreFunc]['Vars'] = varsLocalesDir
	# Eliminar las variables que ya se guardaron como locales
	remove = [k for k in auxVarsDir]
	for k in remove: del auxVarsDir[k]

	# Copia solo las variables que son matrices
	for elem in auxMatrixVarsDir:
		varsLocalesDir[elem] = auxMatrixVarsDir[elem]
		varsLocalesDir[elem]['Scope'] = 'Local'
		varsLocalesDir[elem]['Tipo'] = auxMatrixVarsDir[elem]['Tipo']
	contNumLocales += len(auxMatrixVarsDir)
	dirproc[nombreFunc]['NumLocales'] = contNumLocales
	dirproc[nombreFunc]['Vars'] = varsLocalesDir
	# Eliminar las variables que ya se guardaron como globales
	remove = [k for k in auxMatrixVarsDir]
	for k in remove: del auxMatrixVarsDir[k]


# Funcion para dar de alta en el DirProc las funciones que crea el usuario
def p_altaFuncion(p):
	'''altaFuncion :'''
	global nombreFunc
	global varsLocalesDir
	global funcActual
	global scope 
	global totalInts
	global totalFloats
	global totalStrings
	global totalBools

	resetMemoriaLocal()
	totalFloats = 0
	totalStrings = 0
	totalInts = 0
	totalBools = 0
	# Reinicializa diccionario de variables locales
	scope = "Local"
	varsLocalesDir = {}
	nombreFunc = p[-1]
	dirFunc = set_dir_global(p[-2],1)
	if nombreFunc != "MAIN":
		if not nombreFunc in dirproc:
			funcActual = nombreFunc
			dirproc[nombreFunc] = {}
			dirproc[nombreFunc] = {'Dir':dirFunc,'Tipo': p[-2], 'Vars': {}}
		else:
			print 'Ya existe una funcion con el nombre "%s"' % nombreFunc
			sys.exit()
	else:
		sys.exit('La funcion no puede llamarse main')


	

def p_altaInicioFunc(p):
	'''altaInicioFunc :'''
	global funcActual

	inicio = altaInicioFunc()
	dirproc[funcActual]['Inicio'] = inicio

def p_g(p):
	'''g : INT
			| BOOL
			| FLOAT
			| VOID'''
	p[0] = p[1]

def p_h(p):
	'''h : param 
			|'''
	global varsList
	global auxVarsDir
	global varsLocalesDir
	global paramsList
	# Copia solo las variables locales como parametros
	dirproc[nombreFunc]['NumParams'] = len(auxVarsDir)
	dirproc[nombreFunc]['OrderedParams'] = paramsList
	varsLocalesDir = {}
	auxVarsDir = {}
	paramsList = []

def p_param(p):
	'''param : ID COLON tipo saveParamVar j'''

def p_saveParamVar(p):
	'''saveParamVar :'''
	global varsList
	global auxVarsDir
	global totalStrings
	global totalInts
	global totalFloats
	global totalBools
	global paramsList
	
	# Obtiene el nombre de la variable de parametro 
	paramID = p[-3]
	paramsList.append(paramID)
	# Obtiene el tipo de la variable de parametro 
	tipo = p[-1]
	# Le asigna una direccion a la variable
	if tipo == 'int':
		totalInts += 1
	elif tipo == 'float':
		totalFloats += 1
	elif tipo == 'string':
		totalStrings += 1
	elif tipo == 'bool':
		totalBools += 1

	assignedDir = set_dir_local(tipo,1)
	# Guarda en un diccionario el nombre, tipo y direccion.
	auxVarsDir[paramID] = {'Tipo' : tipo, 'Dir' : assignedDir, 'Scope' : 'Local'}
	dirproc[nombreFunc]['Params'] = auxVarsDir

def p_j(p):
	'''j : COMMA param
			|'''

def p_main(p):
	'''main : MAIN altaMain LPARENTHESIS RPARENTHESIS k bloque SEMICOLON ENDFUNC'''
	global totalStrings
	global totalInts
	global totalFloats
	global totalBools

	totalTemps = generaAccionRetorno(funcActual)
	dirproc[funcActual]['Tamano'] = {'ints' : totalInts, 'floats' : totalFloats, 'bools' : totalBools, 'strings' : totalStrings, 'tempInts' : totalTemps['totalTempInts'], 'tempFloats' : totalTemps['totalTempFloats'], 'tempBools' : totalTemps['totalTempBools'], 'tempStrings' : totalTemps['totalTempStrings']}
	generaAccionEndMain()

# Funcion para dar de alta el main en el DirProc
def p_altaMain(p):
	'''altaMain :'''
	global nombreFunc
	global varsLocalesDir
	global funcActual
	global scope 
	global totalInts
	global totalFloats
	global totalStrings
	global totalBools

	
	# Reinicializa diccionario de variables locales
	totalFloats = 0
	totalStrings = 0
	totalInts = 0
	totalBools = 0
	resetMemoriaLocal()
	varsLocalesDir = {}
	scope = "Local"
	nombreFunc = 'main'
	funcActual = nombreFunc
	dirproc[nombreFunc] = {}
	dirproc[nombreFunc] = {'Tipo': 'void', 'Vars': {}}
	iniciaMain()

def p_k(p):
	'''k : vars
			|'''
	global varsList
	global auxVarsDir
	global varsLocalesDir
	global auxMatrixVarsDir
	# Copia solo las variables locales
	for elem in auxVarsDir:
		varsLocalesDir[elem] = auxVarsDir[elem]
		varsLocalesDir[elem]['Scope'] = 'Local'
		varsLocalesDir[elem]['Tipo'] = auxVarsDir[elem]['Tipo']
		varsLocalesDir[elem]['Valor'] = None
	dirproc[nombreFunc]['Vars'] = varsLocalesDir

	# Copia solo las variables que son matrices
	for elem in auxMatrixVarsDir:
		varsLocalesDir[elem] = auxMatrixVarsDir[elem]
		varsLocalesDir[elem]['Scope'] = 'Local'
		varsLocalesDir[elem]['Tipo'] = auxMatrixVarsDir[elem]['Tipo']
	dirproc[nombreFunc]['Vars'] = varsLocalesDir


def p_bloque(p):
	'''bloque : LBRACKET l RBRACKET'''

def p_l(p):
	'''l : estatuto l
			|'''

def p_estatuto(p):
	'''estatuto : estatutotipos SEMICOLON'''

def p_estatutotipos(p):
	'''estatutotipos : asignacion
			| condicion
			| ciclo
			| escritura
			| llamadafunc
			| specialfunc
			| return'''

def p_asignacion(p):
	'''asignacion : ID exp_asign accessMatrix EQUAL exp_12 expresion exp_13'''

def p_exp_asign(p):
	'''exp_asign :'''
	global varActual
	varActual = p[-1]
	# Busca variable en variables locales del proc
	try:
		temp_dirvar = dirproc[funcActual]['Vars'][p[-1]]['Dir']
		temp_tipovar = dirproc[funcActual]['Vars'][p[-1]]['Tipo']
		exp_1(temp_dirvar,temp_tipovar)
	except KeyError as key:
		# Busca variable en parametros  del proc
		try:
			temp_dirvar = dirproc[funcActual]['Params'][p[-1]]['Dir']
			temp_tipovar = dirproc[funcActual]['Params'][p[-1]]['Tipo']
			exp_1(temp_dirvar,temp_tipovar)
		except KeyError as key:
			# Si no lo encuentra, busca variable en proc global
			try:
				temp_dirvar = dirproc[funcGlobal]['Vars'][p[-1]]['Dir'];
				temp_tipovar = dirproc[funcGlobal]['Vars'][p[-1]]['Tipo'];
				exp_1(temp_dirvar,temp_tipovar)	
			except KeyError as key:
				print 'Variable %s no esta declarada' % key
				sys.exit()

	
	
	

def p_exp_12(p):
	'''exp_12 :'''
	exp_12(p[-1])

def p_exp_13(p):
	'''exp_13 :'''
	exp_13()

def p_accessMatrix(p):
	'''accessMatrix : LSQUAREBRACKET acceso_dimvar_2 exp acceso_dimvar_3 RSQUAREBRACKET acceso_dimvar_4 LSQUAREBRACKET exp acceso_dimvar_3 RSQUAREBRACKET acceso_dimvar_5
			|'''

def p_acceso_dimvar_2(p):
	'''acceso_dimvar_2 :'''
	
	global varActual
	try:
		accessingMatrix = dirproc[funcActual]['Vars'][varActual]
		acceso_dimvar_2(accessingMatrix)
	except KeyError as key:
		try:
			accessingMatrix = dirproc[funcGlobal]['Vars'][varActual]
			acceso_dimvar_2(accessingMatrix)
		except KeyError as key:
			print 'Variable %s no es dimensionada' % key
			sys.exit()

def p_acceso_dimvar_3(p):
	'''acceso_dimvar_3 :'''
	acceso_dimvar_3()



def p_acceso_dimvar_4(p):
	'''acceso_dimvar_4 :'''
	acceso_dimvar_4()

def p_acceso_dimvar_5(p):
	'''acceso_dimvar_5 :'''
	acceso_dimvar_5()
def p_expresion(p):
	'''expresion : specialexp m exp_9 n'''

def p_m(p):
	'''m : o exp_8 specialexp
			|'''

def p_o(p):
	'''o : AND
			| OR'''
	p[0] = p[1]

def p_exp_8(p):
	'''exp_8 :'''
	exp_8(p[-1])

def p_exp_9(p):
	'''exp_9 :'''
	exp_9()

def p_n(p):
	'''n : expresion
			|'''

def p_specialexp(p):
	'''specialexp : exp p exp_11'''

def p_p(p):
	'''p : q exp_10 exp
			|'''

def p_q(p):
	'''q : GREATERTHAN
			| LESSTHAN
			| NOTEQUAL
			| LESSEQUAL
			| GREATEREQUAL
			| EQUALEQUAL'''
	p[0] = p[1]

def p_exp_10(p):
	'''exp_10 :'''
	exp_10(p[-1])

def p_exp_11(p):
	'''exp_11 :'''
	exp_11()

def p_exp(p):
	'''exp : termino exp_5 ab'''

def p_exp_5(p):
	'''exp_5 :'''
	exp_5()

def p_ab(p):
	'''ab : ab2 exp_3 exp
			|'''

def p_ab2(p):
	'''ab2 : PLUS
			| MINUS'''
	# Envia signo + o -
	p[0] = p[1]

def p_exp_3(p):
	'''exp_3 :'''
	# Meter op(+ -) en POper
	exp_3(p[-1])

def p_termino(p):
	'''termino : factor exp_4 ac'''

def p_exp_4(p):
	# Si top(pOper) es * o /
	'''exp_4 :'''
	exp_4()


def p_ac(p):
	'''ac : ac2 exp_2 termino
			|'''

def p_exp_2(p):
	'''exp_2 :'''
	# Meter op(* /) en POper
	exp_2(p[-1])

def p_ac2(p):
	'''ac2 : PRODUCT
			| DIVISION'''
	# Envia signo * o /
	p[0] = p[1]

def p_factor(p):
	'''factor : ad
			| ae
			| af
			| opfunc'''

def p_ad(p):
	'''ad : LPARENTHESIS exp_6 expresion RPARENTHESIS exp_7'''

def p_exp_6(p):
	'''exp_6 :'''
	exp_6()

def p_exp_7(p):
	'''exp_7 :'''
	exp_7()

def p_ae(p):
	'''ae : ag varcte'''

def p_af(p):
	'''af : llamadafunc'''

def p_ag(p):
	'''ag : PLUS
			| MINUS
			|'''

def p_varcte(p):
	'''varcte : CTEINT exp_cte_int
			| CTEFLOAT exp_cte_float
			| ctebool exp_cte_bool
			| CTESTRING exp_cte_string
			| ID exp_1 accessMatrix '''

def p_exp_cte_int(p):
	'''exp_cte_int :'''
	global memIntCte
	global totalCtesInts
	temp_tipocte = "int"
	
	# Busca constante encontrada en tabla de constantes, si no existe la crea
	if not p[-1] in tablaConstantes:
		tablaConstantes[p[-1]] = {"Dir":memIntCte, "Tipo":temp_tipocte}
		exp_1(memIntCte,temp_tipocte)	
		memIntCte += 1
		totalCtesInts += 1
	else:
		exp_1(tablaConstantes[p[-1]]["Dir"],temp_tipocte)	
	
	
	

def p_exp_cte_float(p):
	'''exp_cte_float :'''
	'''exp_cte_int :'''
	global memFloatCte
	global totalCtesFloats

	temp_tipocte = "float"
	# Busca constante encontrada en tabla de constantes, si no existe la crea
	if not p[-1] in tablaConstantes:
		tablaConstantes[p[-1]] = {"Dir":memFloatCte, "Tipo":temp_tipocte}
		exp_1(memFloatCte,temp_tipocte)	
		memFloatCte += 1
		totalCtesFloats += 1
	else:
		exp_1(tablaConstantes[p[-1]]["Dir"],temp_tipocte)
	
	

def p_ctebool(p):
	'''ctebool : TRUE
			| FALSE'''
	p[0] = p[1]

def p_exp_cte_bool(p):
	'''exp_cte_bool :'''
	global memBoolCte
	global totalCtesBools

	temp_tipocte = "bool"
	# Busca constante encontrada en tabla de constantes, si no existe la crea
	if not p[-1] in tablaConstantes:
		tablaConstantes[p[-1]] = {"Dir":memBoolCte, "Tipo":temp_tipocte}
		exp_1(memBoolCte,temp_tipocte)
		memBoolCte += 1
		totalCtesBools += 1
	else:
		exp_1(tablaConstantes[p[-1]]["Dir"],temp_tipocte)
	
	

def p_exp_cte_string(p):
	'''exp_cte_string :'''
	global memStringCte
	global totalCtesStrings

	temp_tipocte = "string"
	# Busca constante encontrada en tabla de constantes, si no existe la crea
	if not p[-1] in tablaConstantes:
		tablaConstantes[p[-1]] = {"Dir":memStringCte, "Tipo":temp_tipocte}
		exp_1(memStringCte,temp_tipocte)	
		memStringCte += 1
		totalCtesStrings += 1
	else:
		exp_1(tablaConstantes[p[-1]]["Dir"],temp_tipocte)
	
	
def p_exp_1(p):
	'''exp_1 :'''
	global varActual
	varActual = p[-1]
	# Busca variable en variables local en proc actual
	try:
		temp_dirvar = dirproc[funcActual]['Vars'][p[-1]]['Dir']
		temp_tipovar = dirproc[funcActual]['Vars'][p[-1]]['Tipo']
		exp_1(temp_dirvar,temp_tipovar)	
	except KeyError as key:
		# Busca variable en parametros del proc actual
		try:
			temp_dirvar = dirproc[funcActual]['Params'][p[-1]]['Dir']
			temp_tipovar = dirproc[funcActual]['Params'][p[-1]]['Tipo']
			exp_1(temp_dirvar,temp_tipovar)	
		except KeyError as key:
			# Si no lo encuentra, busca variable en proc global
			try:
				temp_dirvar = dirproc[funcGlobal]['Vars'][p[-1]]['Dir'];
				temp_tipovar = dirproc[funcGlobal]['Vars'][p[-1]]['Tipo'];
				exp_1(temp_dirvar,temp_tipovar)	
			except KeyError as key:
				print 'Variable %s no esta declarada' % key
				sys.exit()

	

		

def p_condicion(p):
	'''condicion : IF LPARENTHESIS expresion RPARENTHESIS estatuto_if_1 bloque s estatuto_endif'''

def p_estatuto_if_1(p):
	'''estatuto_if_1 :'''
	estatuto_if_1()

def p_s(p):
	'''s : ELSE estatuto_else bloque
			|'''
def p_estatuto_else(p):
	'''estatuto_else :'''
	estatuto_else()

def p_estatuto_endif(p):
	'''estatuto_endif :'''
	estatuto_endif()

def p_ciclo(p):
	'''ciclo : WHILE estatuto_while_1 LPARENTHESIS expresion RPARENTHESIS estatuto_while_2 bloque estatuto_while_3'''

def p_estatuto_while_1(p):
	'''estatuto_while_1 :'''
	estatuto_while_1()

def p_estatuto_while_2(p):
	'''estatuto_while_2 :'''
	estatuto_while_2()

def p_estatuto_while_3(p):
	'''estatuto_while_3 :'''
	estatuto_while_3()

def p_escritura(p):
	'''escritura : PRINT LPARENTHESIS ah RPARENTHESIS'''

def p_estatuto_print(p):
	'''estatuto_print :'''
	estatuto_print()

def p_ah(p):
	'''ah : expresion estatuto_print ai
			| CTESTRING estatuto_print ai'''

def p_ai(p):
	'''ai : COMMA ah
			|'''

def p_llamadafunc(p):
	'''llamadafunc : CALL ID estatuto_llamadafunc_1 LPARENTHESIS estatuto_llamadafunc_2 t estatuto_llamadafunc_5 RPARENTHESIS estatuto_llamadafunc_6'''

def p_estatuto_llamadafunc_1(p):
	'''estatuto_llamadafunc_1 :'''
	global funcLlamada
	funcLlamada = p[-1]
	if not funcLlamada in dirproc:
		print 'Funcion %s no existe' % funcLlamada
		sys.exit()

def p_estatuto_llamadafunc_2(p):
	'''estatuto_llamadafunc_2 :'''
	global paramCounter

	# Genera accion ERA , manda funcion a la que llama
	tamMemoriaLocalLlamadaFunc = dirproc[funcLlamada]['NumLocales'] + dirproc[funcLlamada]['NumParams']
	estatuto_llamadafunc_2(funcLlamada, tamMemoriaLocalLlamadaFunc)
	paramCounter = 0

def p_t(p):
	'''t : u
			|'''

def p_u(p):
	'''u : exp estatuto_llamadafunc_3
			| exp estatuto_llamadafunc_3 COMMA estatuto_llamadafunc_4 u'''

def p_estatuto_llamadafunc_3(p):
	'''estatuto_llamadafunc_3 :'''
	global paramCounter
	try:
		paramActual = dirproc[funcLlamada]['OrderedParams'][paramCounter]
		dirParamActual = dirproc[funcLlamada]['Params'][paramActual]['Dir']
		tipoParamActual = dirproc[funcLlamada]['Params'][paramActual]['Tipo']
		# manda param actual y su tipo
		estatuto_llamadafunc_3(dirParamActual, tipoParamActual)
	except IndexError:
		sys.exit("Numero de parametros es mayor que el numero de argumentos")
	
	
def p_estatuto_llamadafunc_4(p):
	'''estatuto_llamadafunc_4 :'''
	global paramCounter
	paramCounter += 1

def p_estatuto_llamadafunc_5(p):
	'''estatuto_llamadafunc_5 :'''
	global paramCounter

	if dirproc[funcLlamada]['NumParams'] > 0 and not paramCounter == dirproc[funcLlamada]['NumParams'] - 1:
		sys.exit("Numero de parametros no coincide con el numero de argumentos")
		
def p_estatuto_llamadafunc_6(p):
	'''estatuto_llamadafunc_6 :'''
	quadInicioFuncLlamada = dirproc[funcLlamada]['Inicio']
	tipoFuncLlamada = dirproc[funcLlamada]['Tipo']
	dirFuncLlamada = dirproc[funcLlamada]['Dir']
	estatuto_llamadafunc_6(funcLlamada, quadInicioFuncLlamada, tipoFuncLlamada, dirFuncLlamada)



def p_return(p):
	'''return : RETURN exp'''
	global funcActual
	tipoFuncActual = dirproc[funcActual]['Tipo']
	estatuto_return(funcActual, tipoFuncActual)

def p_specialfunc(p):
	'''specialfunc : opfunc
			| dibujafunc'''

def p_opfunc(p):
	'''opfunc : randomfunc'''

def p_randomfunc(p):
	'''randomfunc : RANDOM LPARENTHESIS exp COMMA exp RPARENTHESIS'''
	opfunc_random()

def p_dibujafunc(p):
	'''dibujafunc : al am an'''

def p_al(p):
	'''al : linewidthfunc
			|'''

def p_am(p):
	'''am : linecolorfunc
			|'''

def p_an(p):
	'''an : dibuja 
			| startfillfunc dibuja SEMICOLON loopDibuja stopfillfunc'''

def p_loopDibuja(p):
	'''loopDibuja : dibuja SEMICOLON loopDibuja
			|'''

def p_linewidthfunc(p):
	'''linewidthfunc : LINEWIDTH LPARENTHESIS exp RPARENTHESIS SEMICOLON'''
	dibujafunc_linewidth()

def p_linecolorfunc(p):
	'''linecolorfunc : LINECOLOR LPARENTHESIS exp COMMA exp COMMA exp RPARENTHESIS SEMICOLON'''
	dibujafunc_linecolor()

def p_dibuja(p):
	'''dibuja : v RPARENTHESIS'''

def p_v(p):
	'''v : LINE lineparam
			| SQUARE squareparam
			| CIRCLE circleparam
			| STAR starparam
			| TRIANGLE triangleparam
			| ARC arcparam'''

def p_lineparam(p):
	'''lineparam : LPARENTHESIS exp COMMA exp COMMA exp COMMA exp'''
	dibujafunc_line()

def p_squareparam(p):
	'''squareparam : LPARENTHESIS exp COMMA exp COMMA exp'''
	dibujafunc_square()

def p_circleparam(p):
	'''circleparam : LPARENTHESIS exp COMMA exp COMMA exp'''
	dibujafunc_circle()
def p_starparam(p):
	'''starparam : LPARENTHESIS exp COMMA exp COMMA exp'''
	dibujafunc_star()

def p_triangleparam(p):
	'''triangleparam : LPARENTHESIS exp COMMA exp COMMA exp'''
	dibujafunc_triangle()

def p_arcparam(p):
	'''arcparam : LPARENTHESIS exp COMMA exp COMMA exp COMMA exp COMMA exp'''
	dibujafunc_arc()

def p_startfillfunc(p):
	'''startfillfunc : STARTFILL LPARENTHESIS exp COMMA exp COMMA exp RPARENTHESIS SEMICOLON'''
	dibujafunc_startfill()

def p_stopfillfunc(p):
	'''stopfillfunc : STOPFILL LPARENTHESIS RPARENTHESIS'''
	dibujafunc_stopfill()

def p_error(p):
    print('Syntax error in token %s with value %s in line %s' % (p.type, p.value, p.lineno))
    sys.exit()

# Build the parser
dmcparser = yacc.yacc()
# Main 
if __name__ == '__main__':
	# Revisa si el archivo se dio como input
	if (len(sys.argv) > 1):
		file = sys.argv[1]
		# Abre el archivo, almacena su informacion y lo cierra
		try:
			f = open(file,'r')
			data = f.read()
			f.close()
			# Parse the data
			
			if (dmcparser.parse(data, tracking=True) == 'Success'):
				print "Valid"
				
				for key, value in dirproc.iteritems():
					print key, value
					print "\n"

				print "Tabla de Constantes"
				print tablaConstantes
				printPilas()

				'''
				============================================
				Manda llamar a la maquina virtual
				============================================
				'''
				memGlobal = Memoria(dirproc[funcGlobal]['Tamano']['ints'],dirproc[funcGlobal]['Tamano']['floats'],dirproc[funcGlobal]['Tamano']['strings'],dirproc[funcGlobal]['Tamano']['bools'],dirproc[funcGlobal]['Tamano']['tempInts'],dirproc[funcGlobal]['Tamano']['tempFloats'], dirproc[funcGlobal]['Tamano']['tempStrings'], dirproc[funcGlobal]['Tamano']['tempBools'])
				memActiva = Memoria(dirproc['main']['Tamano']['ints'],dirproc['main']['Tamano']['floats'],dirproc['main']['Tamano']['strings'],dirproc['main']['Tamano']['bools'],dirproc['main']['Tamano']['tempInts'],dirproc['main']['Tamano']['tempFloats'], dirproc['main']['Tamano']['tempStrings'], dirproc['main']['Tamano']['tempBools'])
				memCtes = Memoria(totalCtesInts,totalCtesFloats,totalCtesStrings,totalCtesBools,0,0,0,0)


				for key, elems in tablaConstantes.iteritems():
					direccion = elems['Dir']
					valor = key
					memCtes.set_valor_memoria(valor, direccion)


				#print memCtes.get_valor_memoria(12000)

				cuadruplos = getCuadruplos()
				initMaquinaVirtual(dirproc, memGlobal, memActiva, memCtes, cuadruplos)
			

		except EOFError:
	   		print(EOFError)
	else:
		print('File missing')
