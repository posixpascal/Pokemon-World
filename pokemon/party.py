class Party:
	def __init__(self):
		self.party = {}
		
	def show(self):
		return self.party
		
	def add(self, pkmn):
		if len(self.party.items()) == 6:
			return False
		else: self.party[len(self.party.items()) + 1] = pkmn
	
	def remove(self, id):
		self.party[id] = {}
		
