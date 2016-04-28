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
	

	def set_valor_memoria(self, valor, direccion):
		offset = self.get_offset(direccion)
		memoria = self.get_memoria(direccion)
		memoria[direccion - offset] = valor

	def get_valor_memoria(self, direccion):
		offset = self.get_offset(direccion)
		memoria = self.get_memoria(direccion)
		return memoria[direccion - offset]


		
	def get_offset(self, direccion):
		if direccion>=1 and direccion<4000:
			if direccion>=1 and direccion<1000:
				return 1
			if direccion>=1000 and direccion<2000:
				return 1000
			if direccion>=2000 and direccion<3000:
				return 2000
			if direccion>=3000 and direccion<4000:
				return 3000
		if direccion>=4000 and direccion<8000:
			if direccion>=4000 and direccion<5000:
				return 4000
			if direccion>=5000 and direccion<6000:
				return 5000
			if direccion>=6000 and direccion<7000:
				return 6000
			if direccion>=7000 and direccion<8000:
				return 7000
		if direccion>=8000 and direccion<12000:
			if direccion>=8000 and direccion<9000:
				return 8000
			if direccion>=9000 and direccion<10000:
				return 9000
			if direccion>=10000 and direccion<11000:
				return 10000
			if direccion>=11000 and direccion<12000:
				return 11000
		if direccion>=12000 and direccion<16000:
			if direccion>=12000 and direccion<13000:
				return 12000
			if direccion>=13000 and direccion<14000:
				return 13000
			if direccion>=14000 and direccion<15000:
				return 14000
			if direccion>=15000 and direccion<16000:
				return 15000



	def get_memoria(self, direccion):
		if direccion >=8000 and direccion<12000:
			if direccion>=8000 and direccion<9000:
				return self.tempInts
			if direccion>=9000 and direccion<10000:
				return self.tempFloats
			if direccion>=10000 and direccion<11000:
				return self.tempBools
			if direccion>=11000 and direccion<12000:
				return self.tempStrings
		else:
			if (direccion>=1 and direccion<1000) or (direccion>=4000 and direccion<5000) or (direccion>=12000 and direccion<13000):
				return self.ints
			if (direccion>=1000 and direccion<2000) or (direccion>=5000 and direccion<6000) or (direccion>=13000 and direccion<14000):
				return self.floats
			if (direccion>=2000 and direccion<3000) or (direccion>=6000 and direccion<7000) or (direccion>=14000 and direccion<15000):
				return self.bools
			if (direccion>=3000 and direccion<4000) or (direccion>=7000 and direccion<8000) or (direccion>=15000 and direccion<16000):
				return self.strings

		




