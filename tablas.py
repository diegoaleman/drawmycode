'''
class TablaVariablesNodo:
	def __init__(self, nombre, tipo, direc):
		self.nombre_variable = nombre
		self.tipo_dato = tipo
		self.direccion = direc
		self.valor = None

class TablaProcedimientosNodo:
	def __init__(self, nombre, tipo, dirp):
		self.nombre_proc = nombre
		self.tipo_retorno = tipo
		self.dir_proc = dirp
		self.vars = {}
'''
dircproc = {}

contDirInt = 1
contDirFloat = 10000
contDirBool = 20000
contDirString = 30000

# Asigna direccion a una variable de acuerdo a su tipo
def set_dir(tipo):
	global contDirInt
	global contDirFloat
	global contDirBool
	global contDirString

	assignedDir = None
	if tipo == 'int':
		assignedDir = contDirInt
		contDirInt += 1
	elif tipo == 'float':
		assignedDir = contDirFloat
		contDirFloat += 1
	elif tipo == 'bool':
		assignedDir = contDirBool
		contDirBool += 1
	elif tipo == 'string':
		assignedDir = contDirString
		contDirString += 1
	return assignedDir