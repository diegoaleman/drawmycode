class Memoria:
	def __init__(self, ints_espacio, floats_espacio, strings_espacio, bools_espacio, tempInts_espacio, tempFloats_espacio, tempStrings_espacio, tempBools_espacio):
		self.ints = [0] * ints_espacio
		self.floats = [0.0] * floats_espacio
		self.strings = [''] * strings_espacio
		self.bools = [False] * bools_espacio
		self.tempInts = [0] * tempInts_espacio
		self.tempFloats = [0.0] * tempFloats_espacio
		self.tempStrings = [''] * tempStrings_espacio
		self.tempBools = [False] * tempBools_espacio
	
