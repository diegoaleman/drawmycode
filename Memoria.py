class MapaMemoria:
	def __init__(self, inicio_int, inicio_float, inicio_string, inicio_bool,limite):
		self.int = [ inicio_int, 0 ]
		self.float = [ inicio_float, 0 ]
		self.string = [ inicio_string, 0 ]
		self.bool= [inicio_bool,0]
		self.limite = limite

	def add_int(self, cant):
		if ( self.int[0] + self.int[1] + cant ) < self.float[0]:
			self.int[1] += cant
			return ( self.int[0] + self.int[1] - cant )
		else:
			print 'STACKOVERFLOW: stack pointer exceeded the stack bound.'

	def add_float(self, cant):
		if ( self.float[0] + self.float[1] + cant ) < self.string[0]:
			self.float[1] += cant
			return ( self.float[0] + self.float[1] - cant )
		else:
			print 'STACKOVERFLOW: stack pointer exceeded the stack bound.'

	def add_string(self, cant):
		if ( self.string[0] + self.string[1] + cant ) < self.bool[0]:
			self.string[1] += cant
			return ( self.string[0] + self.string[1] - cant )
		else:
			print 'STACKOVERFLOW: Stack pointer exceeded the stack bound.'

	def add_bool(self, cant):
		if ( self.bool[0] + self.bool[1] + cont ) < self.limite:
			self.bool[1] += cont
			return ( self.bool[0] + self.bool[1] - cont )
		else:
			print 'STACKOVERFLOW: Stack pointer exceeded the stack bound.'

	def add_type(self,tipo,cant):
		if tipo== 'string':
		   return self.add_string(1)
		elif tipo=='int':
		   return self.add_int(1)
		elif tipo=='float':
		   return self.add_float(1)
		elif tipo=='bool':
			return self.add_bool(1)
		elif tipo=='arrint':
		   return self.add_int(int(cant))