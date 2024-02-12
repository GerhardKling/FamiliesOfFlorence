"""
Spouses
"""

import random

class Spouse():
	def __init__(self, name, gender, age):
		self.name = name
		self.gender = gender
		self.age = age
		self.alive = True
		self.inherit = False

	def check_alive(self):
		"""Checks whether player is alive"""
		prob = random.uniform(0, 1)
		if self.age < 5:
			if prob < 0.1:
				self.alive = False
		elif self.age < 50:
			if prob < 0.01:
				self.alive = False
		elif self.age < 60:
			if prob < 0.03:
				self.alive = False
		elif self.age < 70:
			if prob < 0.10:
				self.alive = False
		elif self.age < 80:
			if prob < 0.20:
				self.alive = False			
		elif self.age >= 80: 
			if prob < 0.30:
				self.alive = False	
		else:
			self.alive = True