# ------------------------------------------------------------
# Omar Antonio Carreon Medrano A01036074
# Diego Aleman A01139700
# dmclex.py

# Run:
# python dmclex.py
# python dmcparser.py test/test1.txt

# *Change the test filename to test other files
# ------------------------------------------------------------
import ply.lex as lex

# Lista de palabras reservadas
reserved = {
	'if' : 'IF',
	'else' : 'ELSE',
	'print' : 'PRINT',
	'program' : 'PROGRAM',
	'var' : 'VAR',
	'int' : 'INT',
	'float' : 'FLOAT',
  'begin' : 'BEGIN',
  'end' : 'END',
  'bool' : 'BOOL',
  'string' : 'STRING',
  'func' : 'FUNC',
  'void' : 'VOID',
  'main' : 'MAIN',
  'while' : 'WHILE',
  'return' : 'RETURN',
  'random' : 'RANDOM',
  'lineWidth' : 'LINEWIDTH',
  'lineColor' : 'LINECOLOR',
  'line' : 'LINE',
  'square' : 'SQUARE',
  'circle' : 'CIRCLE',
  'star' : 'STAR',
  'triangle' : 'TRIANGLE',
  'arc' : 'ARC',
  'startFill' : 'STARTFILL',
  'stopFill' : 'STOPFILL',
  'and' : 'AND',
  'or' : 'OR',
  'True' : 'TRUE',
  'False' : 'FALSE',
  'endfunc' : 'ENDFUNC',
  'call' : 'CALL'
}

# Lista de tokens
tokens = ( 'PROGRAM','CTESTRING','COLON', 'SEMICOLON','VAR', 'NOTEQUAL', 'LESSTHAN', 
           'GREATERTHAN', 'IF', 'LBRACKET', 'RBRACKET', 'PLUS', 'MINUS', 
           'PRODUCT', 'DIVISION', 'COMMA', 'EQUAL', 'PRINT', 'LPARENTHESIS', 
           'RPARENTHESIS', 'ELSE', 'ID','INT', 'FLOAT', 'CTEINT', 'CTEFLOAT', 'BEGIN',
           'END','BOOL','STRING','FUNC','VOID','MAIN','WHILE','RETURN','RANDOM','LINEWIDTH',
           'LINECOLOR','LINE','SQUARE','CIRCLE','STAR','TRIANGLE','ARC','STARTFILL','STOPFILL',
           'LESSEQUAL','GREATEREQUAL','EQUALEQUAL','LSQUAREBRACKET','RSQUAREBRACKET',
           'AND','OR','TRUE','FALSE', 'ENDFUNC','CALL')

# Expresiones regulares para los tokens sencillos
t_ignore = ' \t'
t_CTEINT = r'-?[0-9]+'
t_CTEFLOAT = r'-?[0-9]+\.+[0-9]+'
t_COLON	= r':'
t_SEMICOLON	= r';'
t_COMMA	= r','
t_EQUAL	= r'='
t_LESSTHAN = r'<'
t_LESSEQUAL = r'<='
t_GREATERTHAN = r'>'
t_GREATEREQUAL = r'>='
t_NOTEQUAL = r'<>'
t_EQUALEQUAL = r'=='
t_PLUS = r'\+'
t_MINUS = r'-'
t_PRODUCT = r'\*'
t_DIVISION = r'/'
t_LPARENTHESIS = r'\('
t_RPARENTHESIS = r'\)'
t_LSQUAREBRACKET = r'\['
t_RSQUAREBRACKET = r'\]'
t_LBRACKET = r'{'
t_RBRACKET = r'}'

# Expresion regular para los IDs
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

# Expresion regular para las constantes tipo string
def t_CTESTRING(t):  
  r'\".*\"'
  return t

# Regla para identificar saltos de linea y llevar un conteo de la linea actual
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores de lexico
def t_error(t):
    print("Error de lexico %s" % t.value[0])
    exit(-1)
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()