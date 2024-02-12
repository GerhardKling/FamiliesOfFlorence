"""
Weather class
"""

import random

class Weather():
	def __init__(self):
		self.outcome = random.random()
		if self.outcome >= 0.8:
			self.weather = 'excellent'
		elif self.outcome >= 0.5:
			self.weather = 'good'
		elif self.outcome >= 0.3:
			self.weather = 'bad'
		else:
			self.weather = 'terrible'


