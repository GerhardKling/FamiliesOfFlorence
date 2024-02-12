"""
Farm class
"""

class Farm():
	def __init__(self, land):
		self.land = land

	def profit(self, weather, price_grain):
		output = self.land * 10 * weather
		cost = 50/self.land + 0.3 * output
		profit = output * price_grain - cost
		return round(profit, 2)

	def value(self, price_land):
		value = self.land * price_land
		return value
