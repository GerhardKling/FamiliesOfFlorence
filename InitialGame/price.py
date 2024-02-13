"""
Price class
"""

import random
import numpy as np

class Price():
	def __init__(self):
		self.land = abs(random.normalvariate(10, 1))
		self.grain = round(abs(random.normalvariate(0.4, 0.1)), 1)
		self.interest = abs(random.normalvariate(0.05, 0.01))


	def change_land_price(self, game, player):
		"""Adjust price for available land"""
		owned_land = 0
		for fam in game.other_families:
			owned_land += fam.farm		
		#Add ownership of player
		owned_land += len(player.owner)
		#Adjust price
		self.land += 0.5 * (owned_land / game.total_farm - 0.6) + random.normalvariate(0, 0.1)


	def change_grain_prices(self, weather):
		"""Adjust prices based on weather condition"""
		if weather.outcome > 0.7:
			self.grain = np.exp(0.8 * np.log(self.grain) - 0.5)
		else:
			self.grain = np.exp(0.8 * np.log(self.grain) + random.normalvariate(0, 0.1))


	def change_interest_rates(self):
		"""Adjust for player's debt position"""
		self.interest = abs(random.normalvariate(0.05, 0.01))

