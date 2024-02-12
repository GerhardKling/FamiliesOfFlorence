"""
Player class
"""
import random

from farm import Farm

class Player():
	def __init__(self, name, cash = 100, gender = 1):
		self.name = name
		self.cash = cash
		self.owner = []
		self.mill = 0
		self.bakery = 0
		self.brewery = 0
		self.family = ""
		self.debt = 0
		self.age = 16
		self.gender = gender
		self.alive = True
		self.spouse = False	
		self.wealth = 0	

	def buy_farm(self, land, price_land):
		"""Returns Boolean whether one can afford the purchase"""
		farm = Farm(land)
		value = farm.value(price_land)
		if self.cash >= value:
			self.cash -= value
			self.owner.append(farm) #Add to owned property
			return True
		elif self.cash >= 0.5 * value:
			self.debt += value - self.cash
			self.cash = 0
			self.owner.append(farm) #Add to owned property
			return True
		else:
			return False

	def sell_farm(self, price_land):
		"""Returns Boolean whether one can sell a farm"""
		if not self.owner:
			return False
		else:
			value = self.owner[-1].value(price_land)
			self.cash += value
			self.owner.pop(-1)
			return True

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











