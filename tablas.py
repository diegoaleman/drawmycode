'''
	============================================
	Direcciones para variables globales 
	============================================
'''
memGlobalInt = 1
memGlobalIntInicio = 1
memGlobalFloat = 1000
memGlobalFloatInicio = 1000
memGlobalBool = 2000
memGlobalBoolInicio = 2000
memGlobalString = 3000
memGlobalStringInicio = 3000

'''
	============================================
	Direcciones para variables locales y params
	============================================
'''
memLocalInt = 4000
memLocalIntInicio = 4000
memLocalFloat = 5000
memLocalFloatInicio = 5000
memLocalBool = 6000
memLocalBoolInicio = 6000
memLocalString = 7000
memLocalStringInicio = 7000

'''
	============================================
	Direcciones para variables temporales
	============================================
'''
memIntTemp = 8000
memIntTempInicio = 8000
memFloatTemp = 9000
memFloatTempInicio = 9000
memBoolTemp = 10000
memBoolTempInicio = 10000
memStringTemp = 11000
memStringTempInicio = 11000

'''
	============================================
	Direcciones para constantes
	============================================
'''
memIntCte = 12000
memIntCteInicio = 12000
memFloatCte = 13000
memFloatCteInicio = 13000
memBoolCte = 14000
memBoolCteInicio = 14000
memStringCte = 15000
memStringCteInicio = 15000


'''
	=======================================================================
	Reinicar contadores de direcciones de memoria de variables y constantes
	========================================================================
'''
def resetMemoriaLocal():
	global memLocalInt
	global memLocalFloat
	global memLocalBool
	global memLocalString
	global memIntTemp
	global memFloatTemp
	global memBoolTemp
	global memStringTemp
	memLocalInt = memLocalIntInicio
	memLocalFloat = memLocalFloatInicio
	memLocalBool = memLocalBoolInicio
	memLocalString = memLocalStringInicio 
	memIntTemp = memIntTempInicio
	memFloatTemp = memFloatTempInicio
	memBoolTemp = memBoolTempInicio
	memStringTemp = memStringTempInicio


'''
	========================================================================
	Asigna direccion de memoria a una variable global de acuerdo a su tipo
	========================================================================
'''

def set_dir_global(tipo, cant):
	global memGlobalInt
	global memGlobalFloat
	global memGlobalBool
	global memGlobalString

	assignedDir = None
	if tipo == 'int':
		assignedDir = memGlobalInt
		memGlobalInt += cant
	elif tipo == 'float':
		assignedDir = memGlobalFloat
		memGlobalFloat += cant
	elif tipo == 'bool':
		assignedDir = memGlobalBool
		memGlobalBool += cant
	elif tipo == 'string':
		assignedDir = memGlobalString
		memGlobalString += cant
	return assignedDir


'''
	========================================================================
	Asigna direccion de memoria a una variable local de acuerdo a su tipo
	========================================================================
'''
def set_dir_local(tipo, cant):
	global memLocalInt
	global memLocalFloat
	global memLocalBool
	global memLocalString

	assignedDir = None
	if tipo == 'int':
		assignedDir = memLocalInt
		memLocalInt += cant
	elif tipo == 'float':
		assignedDir = memLocalFloat
		memLocalFloat += cant
	elif tipo == 'bool':
		assignedDir = memLocalBool
		memLocalBool += cant
	elif tipo == 'string':
		assignedDir = memLocalString
		memLocalString += cant
	return assignedDir

'''
	=====================================================================
	Genera direccion para el temporal de una operacion para un cuadruplo
	======================================================================
'''
def set_dir_temp(tipoTemp):
	global memIntTemp
	global memFloatTemp
	global memBoolTemp
	global memStringTemp

	if tipoTemp == "int":
		memIntTemp += 1
		dirTemp  = memIntTemp
	elif tipoTemp == "float":
		memFloatTemp +=1
		dirTemp = memFloatTemp
	elif tipoTemp == "bool":
		memBoolTemp +=1
		dirTemp = memBoolTemp
	elif tipoTemp == "String":
		memStringTemp +=1
		dirTemp = memStringTemp
	return dirTemp

def get_Total_Temp_Int():
	return memIntTemp - memIntTempInicio

def get_Total_Temp_Float():
	return memFloatTemp - memFloatTempInicio

def get_Total_Temp_Bool():
	return memBoolTemp - memBoolTempInicio

def get_Total_Temp_String():
	return memStringTemp - memStringTempInicio
'''
	=================================================================
	Regresa variable correspondiente a funcion y direccion de memoria
	=================================================================
'''
def get_var(proc, dire):
	for var, varelems in dirproc[proc]['Vars'].iteritems():
		if varelems['Dir'] == dire:
			return var
