
'''
	============================================
	Direcciones para variables globales y locales
	============================================
'''
contDirInt = 1
contDirFloat = 10000
contDirBool = 20000
contDirString = 30000

'''
	============================================
	Direcciones para variables temporales
	============================================
'''
contDirIntTemp = 1000
contDirFloatTemp = 11000
contDirBoolTemp = 21000
contDirStringTemp = 31000

'''
	============================================
	Direcciones para constantes
	============================================
'''
contDirIntCte = 2000
contDirFloatCte = 12000
contDirBoolCte = 22000
contDirStringCte = 32000

'''
	=====================================================
	Asigna direccion a una variable de acuerdo a su tipo
	=====================================================
'''
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

'''
	=================================================================
	Regresa variable correspondiente a funcion y direccion de memoria
	=================================================================
'''
def get_var(proc, dire):
	for var, varelems in dirproc[proc]['Vars'].iteritems():
		if varelems['Dir'] == dire:
			return var
