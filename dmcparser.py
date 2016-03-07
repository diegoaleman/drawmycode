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

def p_programa(p):
	'''programa : BEGIN PROGRAM ID SEMICOLON a LBRACKET main b RBRACKET SEMICOLON END'''
	p[0] = "Success"


def p_a(p):
	'''a : vars
			|'''


def p_vars(p):
	'''vars : VAR c'''

def p_c(p):
	'''c : f SEMICOLON e'''

def p_f(p):
	'''f : d COLON tipo
			| matrix'''

def p_d(p):
	'''d : ID
			| ID COMMA d'''

def p_tipo(p):
	'''tipo : INT
			| FLOAT
			| BOOL
			| STRING'''


def p_matrix(p):
	'''matrix :  mataux COLON INT'''

def p_mataux(p):
	'''mataux : ID LSQUAREBRACKET CTEINT RSQUAREBRACKET LSQUAREBRACKET CTEINT RSQUAREBRACKET
			| ID LSQUAREBRACKET CTEINT RSQUAREBRACKET LSQUAREBRACKET CTEINT RSQUAREBRACKET COMMA mataux'''

def p_e(p):
	'''e : c 
			|'''

def p_b(p):
	'''b : funcion b
			|'''


def p_funcion(p):
	'''funcion : FUNC g ID LPARENTHESIS h RPARENTHESIS a bloque SEMICOLON'''
	

def p_g(p):
	'''g : INT
			| BOOL
			| FLOAT
			| VOID'''


def p_h(p):
	'''h : param 
			|'''

def p_param(p):
	'''param : ID COLON tipo j'''


def p_j(p):
	'''j : COMMA param
			|'''	
def p_main(p):
	'''main : FUNC VOID MAIN LPARENTHESIS RPARENTHESIS k bloque SEMICOLON'''

def p_k(p):
	'''k : vars
			|'''

def p_bloque(p):
	'''bloque : LBRACKET l RBRACKET'''

def p_l(p):
	'''l : estatuto l
			|'''

def p_estatuto(p):
	'''estatuto : asignacion
			| condicion
			| ciclo
			| escritura
			| llamadafunc
			| specialfunc
			| return'''

def p_asignacion(p):
	'''asignacion : ID aa EQUAL expresion SEMICOLON'''

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
			| af'''

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
			| llamadafunc
			|'''

def p_condicion(p):
	'''condicion : IF LPARENTHESIS expresion RPARENTHESIS bloque s SEMICOLON'''

def p_s(p):
	'''s : ELSE bloque
			|'''

def p_ciclo(p):
	'''ciclo : WHILE LPARENTHESIS expresion RPARENTHESIS bloque SEMICOLON'''


def p_escritura(p):
	'''escritura : PRINT LPARENTHESIS ah RPARENTHESIS SEMICOLON'''

def p_ah(p):
	'''ah : expresion ai
			| CTESTRING ai'''

def p_ai(p):
	'''ai : COMMA ah
			|'''

def p_llamadafunc(p):
	'''llamadafunc : LPARENTHESIS t RPARENTHESIS SEMICOLON'''

def p_t(p):
	'''t : u
			|'''

def p_u(p):
	'''u : exp
			| exp COMMA u'''

def p_return(p):
	'''return : RETURN exp'''

def p_specialfunc(p):
	'''specialfunc : aj 
					| ak'''

def p_aj(p):
	'''aj : RANDOM LPARENTHESIS exp COMMA exp RPARENTHESIS SEMICOLON'''

def p_ak(p):
	'''ak : al am an'''

def p_al(p):
	'''al : linewidthp
			|'''

def p_am(p):
	'''am : linecolorp
			|'''

def p_an(p):
	'''an : dibuja 
			| startfillp dibuja stopfill'''


def p_linewidthp(p):
	'''linewidthp : LINEWIDTH LPARENTHESIS exp RPARENTHESIS SEMICOLON'''

def p_linecolorp(p):
	'''linecolorp : LINECOLOR LPARENTHESIS exp RPARENTHESIS SEMICOLON'''


def p_dibuja(p):
	'''dibuja : v RPARENTHESIS SEMICOLON'''

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

def p_startfillp(p):
	'''startfillp : STARTFILL LPARENTHESIS exp RPARENTHESIS SEMICOLON'''

def p_stopfill(p):
	'''stopfill : STOPFILL LPARENTHESIS RPARENTHESIS SEMICOLON'''


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
		except EOFError:
	   		print(EOFError)
	else:
		print('File missing')
