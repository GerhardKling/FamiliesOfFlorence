"""
Family class
"""

class Family():
	def __init__(self, name):
		self.name = name
		self.members = []
		self.extended = []
		self.title = ('Mr', 'Mrs', 0)
		self.history = []
		self.guilds = []
		self.wealth = 0
		self.council = 0
		self.vote_prob = 0
		self.votes = 0

	def add_player_to_family(self, player):
		self.members.append(player)
		player.family = self.name #Give player family name
		
