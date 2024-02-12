"""
Builds a class of other families
"""

class OtherFamily():
	def __init__(self, name, title: tuple, farm: int):
		self.name = name
		self.title = title
		self.farm = farm
		self.wealth = 0
		self.council = 0
		self.vote_prob = 0
		self.votes = 0
