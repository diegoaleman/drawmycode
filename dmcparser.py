# ------------------------------------------------------------
# Omar Antonio Carreon Medrano A01036074
# Diego Aleman A01139700
# dmcparser.py

# Run:
# python dmclex.py
# python dmcparser.py test1.txt

# *Change the test filename to test other files
# ------------------------------------------------------------

import ply.yacc as yacc
import sys

# Get the token map from the lexer.
from dmclex import tokens
dirproc = {}
varsList = []
matrixList = []
auxvars = {}
auxVarsDir = {}
auxMatrixVarsDir = {}
varsGlobalesDir = {}
varsLocalesDir = {}
nombrePrograma = ""
scope = "Global"
nombreFunc = ""
tipo = ""

def p_programa(p):
	'''programa : BEGIN PROGRAM createDirProc ID altaPrograma SEMICOLON a LBRACKET b main RBRACKET SEMICOLON END'''
	p[0] = "Success"

def p_createDirProc(p):
	'''createDirProc :'''
	dirproc = {}

def p_altaPrograma(p):
	'''altaPrograma :'''
	global nombrePrograma
	# Da de alta el programa en el DirProc
	nombre = p[-1]
	nombrePrograma = nombre
	dirproc[nombrePrograma] = {}
	dirproc[nombrePrograma] = {'Tipo': 'programa', 'Vars': {}}
	
def p_a(p):
	'''a : vars
			|'''
	global varsGlobalesDir
	global auxVarsDir
	global varsList
	global auxMatrixVarsDir
	# Copia solo las variables globales
	for elem in auxVarsDir:
		varsGlobalesDir[elem] = auxVarsDir[elem]
		varsGlobalesDir[elem]['Scope'] = 'Global'
		varsGlobalesDir[elem]['Tipo'] = auxVarsDir[elem]['Tipo']
	dirproc[nombrePrograma]['Vars'] = varsGlobalesDir
	# Eliminar las variables que ya se guardaron como globales
	remove = [k for k in auxVarsDir]
	for k in remove: del auxVarsDir[k]

	# Copia solo las variables globales
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

	# Guarda el tipo de la variable en el diccionario auxiliar de variables
	while (len(varsList) > 0):
		auxVarsDir[varsList.pop()] = {'Tipo' : tipo}

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
	global matrixList
	global auxMatrixVarsDir
	
	# Guarda el tipo de la variable en el diccionario auxiliar de variables
	while (len(matrixList) > 0):
		auxMatrixVarsDir[matrixList.pop()] = {'Tipo' : 'int'}

def p_mataux(p):
	'''mataux : ID saveMatrixID LSQUAREBRACKET CTEINT RSQUAREBRACKET LSQUAREBRACKET CTEINT RSQUAREBRACKET
			| ID saveMatrixID LSQUAREBRACKET CTEINT RSQUAREBRACKET LSQUAREBRACKET CTEINT RSQUAREBRACKET COMMA mataux'''

def p_saveMatrixID(p):
	'''saveMatrixID :'''
	matrixList.append(p[-1])

def p_e(p):
	'''e : c 
			|'''

def p_b(p):
	'''b : funcion b
			|'''

def p_funcion(p):
	'''funcion : FUNC g ID altaFuncion LPARENTHESIS h RPARENTHESIS funcvars bloque SEMICOLON'''

def p_funcvars(p):
	'''funcvars : vars
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
	dirproc[nombreFunc]['Vars'] = varsLocalesDir
	# Eliminar las variables que ya se guardaron como locales
	remove = [k for k in auxVarsDir]
	for k in remove: del auxVarsDir[k]

	# Copia solo las variables globales
	for elem in auxMatrixVarsDir:
		varsLocalesDir[elem] = auxMatrixVarsDir[elem]
		varsLocalesDir[elem]['Scope'] = 'Local'
		varsLocalesDir[elem]['Tipo'] = auxMatrixVarsDir[elem]['Tipo']
	dirproc[nombreFunc]['Vars'] = varsLocalesDir
	# Eliminar las variables que ya se guardaron como globales
	remove = [k for k in auxMatrixVarsDir]
	for k in remove: del auxMatrixVarsDir[k]


# Funcion para dar de alta en el DirProc las funciones que crea el usuario
def p_altaFuncion(p):
	'''altaFuncion :'''
	global nombreFunc
	global varsLocalesDir
	# Reinicializa diccionario de variables locales
	varsLocalesDir = {}
	nombreFunc = p[-1]
	dirproc[nombreFunc] = {}
	dirproc[nombreFunc] = {'Tipo': p[-2], 'Vars': {}}

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
	
	# Copia solo las variables locales como parametros
	for elem in auxVarsDir:
		varsLocalesDir[elem] = auxVarsDir[elem]
		varsLocalesDir[elem]['Scope'] = 'Local'
		varsLocalesDir[elem]['Tipo'] = auxVarsDir[elem]['Tipo']
	dirproc[nombreFunc]['Vars'] = varsLocalesDir

def p_param(p):
	'''param : ID COLON tipo saveParamVar j'''

def p_saveParamVar(p):
	'''saveParamVar :'''
	global varsList
	global auxVarsDir
	# Obtiene el nombre de la variable de parametro 
	paramID = p[-3]
	# Obtiene el tipo de la variable de parametro 
	tipo = p[-1]
	# Guarda en un diccionario el nombre y tipo.
	auxVarsDir[paramID] = {'Tipo' : tipo}

def p_j(p):
	'''j : COMMA param
			|'''

def p_main(p):
	'''main : MAIN altaMain LPARENTHESIS RPARENTHESIS k bloque SEMICOLON'''

# Funcion para dar de alta el main en el DirProc
def p_altaMain(p):
	'''altaMain :'''
	global nombreFunc
	global varsLocalesDir
	# Reinicializa diccionario de variables locales
	varsLocalesDir = {}
	nombreFunc = 'main'
	dirproc[nombreFunc] = {}
	dirproc[nombreFunc] = {'Tipo': 'void', 'Vars': {}}

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
	dirproc[nombreFunc]['Vars'] = varsLocalesDir

	# Copia solo las variables globales
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
	'''asignacion : ID aa EQUAL expresion'''

def p_aa(p):
	'''aa : LSQUAREBRACKET exp RSQUAREBRACKET LSQUAREBRACKET exp RSQUAREBRACKET
			|'''

def p_expresion(p):
	'''expresion : specialexp m n'''

def p_m(p):
	'''m : o specialexp
			|'''

def p_o(p):
	'''o : AND
			| OR'''

def p_n(p):
	'''n : expresion
			|'''

def p_specialexp(p):
	'''specialexp : exp p'''

def p_p(p):
	'''p : q exp
			|'''

def p_q(p):
	'''q : GREATERTHAN
			| LESSTHAN
			| NOTEQUAL
			| LESSEQUAL
			| GREATEREQUAL
			| EQUALEQUAL'''

def p_exp(p):
	'''exp : termino ab'''

def p_ab(p):
	'''ab : ab2 exp
			|'''

def p_ab2(p):
	'''ab2 : PLUS
			| MINUS'''

def p_termino(p):
	'''termino : factor ac'''

def p_ac(p):
	'''ac : ac2 termino
			|'''

def p_ac2(p):
	'''ac2 : PRODUCT
			| DIVISION'''


def p_factor(p):
	'''factor : ad
			| ae
			| af
			| opfunc'''

def p_ad(p):
	'''ad : LPARENTHESIS expresion RPARENTHESIS'''

def p_ae(p):
	'''ae : ag varcte'''

def p_af(p):
	'''af : llamadafunc'''

def p_ag(p):
	'''ag : PLUS
			| MINUS
			|'''

def p_varcte(p):
	'''varcte : CTEINT
			| CTEFLOAT
			| CTEBOOL
			| CTESTRING
			| ID r'''

def p_r(p):
	'''r : LSQUAREBRACKET exp RSQUAREBRACKET LSQUAREBRACKET exp RSQUAREBRACKET
			|'''

def p_condicion(p):
	'''condicion : IF LPARENTHESIS expresion RPARENTHESIS bloque s'''

def p_s(p):
	'''s : ELSE bloque
			|'''

def p_ciclo(p):
	'''ciclo : WHILE LPARENTHESIS expresion RPARENTHESIS bloque'''


def p_escritura(p):
	'''escritura : PRINT LPARENTHESIS ah RPARENTHESIS'''

def p_ah(p):
	'''ah : expresion ai
			| CTESTRING ai'''

def p_ai(p):
	'''ai : COMMA ah
			|'''

def p_llamadafunc(p):
	'''llamadafunc : LPARENTHESIS t RPARENTHESIS'''

def p_t(p):
	'''t : u
			|'''

def p_u(p):
	'''u : exp
			| exp COMMA u'''

def p_return(p):
	'''return : RETURN exp'''

def p_specialfunc(p):
	'''specialfunc : opfunc
			| dibujafunc'''

def p_opfunc(p):
	'''opfunc : randomfunc'''

def p_randomfunc(p):
	'''randomfunc : RANDOM LPARENTHESIS exp COMMA exp RPARENTHESIS'''

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
			| startfillfunc dibuja stopfillfunc'''


def p_linewidthfunc(p):
	'''linewidthfunc : LINEWIDTH LPARENTHESIS exp RPARENTHESIS SEMICOLON'''

def p_linecolorfunc(p):
	'''linecolorfunc : LINECOLOR LPARENTHESIS exp RPARENTHESIS SEMICOLON'''


def p_dibuja(p):
	'''dibuja : v RPARENTHESIS'''

def p_v(p):
	'''v : LINE lineparam
			| SQUARE squareparam
			| CIRCLE circleparam
			| STAR  starparam
			| TRIANGLE triangleparam
			| ARC arcparam'''

def p_lineparam(p):
	'''lineparam : LPARENTHESIS exp COMMA exp COMMA exp COMMA exp'''

def p_squareparam(p):
	'''squareparam : LPARENTHESIS exp COMMA exp COMMA exp'''

def p_circleparam(p):
	'''circleparam : LPARENTHESIS exp COMMA exp COMMA exp'''

def p_starparam(p):
	'''starparam : LPARENTHESIS exp COMMA exp COMMA exp'''

def p_triangleparam(p):
	'''triangleparam : LPARENTHESIS exp COMMA exp COMMA exp'''

def p_arcparam(p):
	'''arcparam : LPARENTHESIS exp COMMA exp COMMA exp COMMA exp COMMA exp'''

def p_startfillfunc(p):
	'''startfillfunc : STARTFILL LPARENTHESIS exp RPARENTHESIS SEMICOLON'''

def p_stopfillfunc(p):
	'''stopfillfunc : STOPFILL LPARENTHESIS RPARENTHESIS'''


def p_error(p):
    print('Syntax error in token %s with value %s in line %s' % (p.type, p.value, p.lineno))

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
				print ('Valid program');
				print dirproc
		except EOFError:
	   		print(EOFError)
	else:
		print('File missing')
