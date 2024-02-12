"""
Game class
"""
import random
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

from other_family import OtherFamily
from names import Names

class Game():
	def __init__(self):
		self.players = []
		self.other_families = []
		self.year = 800
		self.total_farm = 0

	def add_player(self, player):
		"""Adds player to game"""
		self.players.append(player)

	def start_other_families(self):
		TITLES = [
		('Mr', 'Mrs', 0),
		('Baronet', 'Baronet', 1),
		('Baron', 'Baroness', 2),
		('Viscount', 'Viscountess', 3),
		('Earl', 'Countess', 4),
		('Marquess', 'Marchioness', 5),
		('Duke', 'Duchess', 6),
		('Royal Duke', 'Royal Duchess', 7),
		('Grand duke', 'Grand duchess', 8),
		]
		names = Names()
		#Create families based on titles
		for title in TITLES:
			if title[2] == 0:
				for idx in range(5):
					other_family = OtherFamily(name = names.last_name[idx], title = title, farm = random.randint(1, 10))
					self.other_families.append(other_family)
			if title[2] == 1:
				for idx in range(5, 9):
					other_family = OtherFamily(name = names.last_name[idx], title = title, farm = random.randint(10, 20))
					self.other_families.append(other_family)
			if title[2] == 2:
				for idx in range(9, 12):
					other_family = OtherFamily(name = names.last_name[idx], title = title, farm = random.randint(15, 25))
					self.other_families.append(other_family)
			if title[2] == 3:
				for idx in range(12, 14):
					other_family = OtherFamily(name = names.last_name[idx], title = title, farm = random.randint(20, 25))
					self.other_families.append(other_family)					
			if title[2] == 4:
				for idx in range(14, 16):
					other_family = OtherFamily(name = names.last_name[idx], title = title, farm = random.randint(25, 30))
					self.other_families.append(other_family)	
			if title[2] == 5:
				for idx in range(16, 17):
					other_family = OtherFamily(name = names.last_name[idx], title = title, farm = random.randint(30, 40))
					self.other_families.append(other_family)	
			if title[2] == 6:
				for idx in range(17, 18):
					other_family = OtherFamily(name = names.last_name[idx], title = title, farm = random.randint(40, 50))
					self.other_families.append(other_family)	
			if title[2] == 7:
				for idx in range(18, 19):
					other_family = OtherFamily(name = names.last_name[idx], title = title, farm = random.randint(50, 60))
					self.other_families.append(other_family)	
			if title[2] == 8:
				for idx in range(19, 20):
					other_family = OtherFamily(name = names.last_name[idx], title = title, farm = random.randint(60, 100))
					self.other_families.append(other_family)	

		#Determine total number of farms
		for fam in self.other_families:
			self.total_farm += fam.farm

		#Add farms not owned by big families
		self.total_farm += random.randint(40, 80)

	def election(self, family, price_land):
		if self.year % 5 == 0:
			tk.messagebox.showinfo(title = 'Elections', message = f'Elections to the City Council commence in the year {self.year}.')

			#Update wealth of other families
			for fam in self.other_families:
				fam.wealth = fam.farm * 10 * price_land

			#Select families for election
			election_roll = []
			election_roll.extend(self.other_families)
			election_roll.append(family)

			#Sort by wealth
			election_roll.sort(reverse= True, key = lambda x: x.wealth)

			#Determine probability to get vote
			for fam in election_roll:
				fam.vote_prob =  min(fam.wealth / price_land * 0.001 + fam.title[2] * 0.02, 0.9)
				if fam.vote_prob < 0.2:
					fam.vote_prob = 0

			#Voting system
			for fam in election_roll:
				for voter in range(1000):
					prob = random.uniform(0, 1)
					if prob <= fam.vote_prob:
						fam.votes += 1

			#Convert votes to seats
			for fam in election_roll:
				fam.council = fam.votes // 50

			#Reset all votes
			for fam in election_roll:
				fam.votes = 0

			#Count number of families with seats
			families_with_seats = [fam for fam in election_roll if fam.council > 0]

			count = len(families_with_seats)

			#Create Numpy array
			y = np.zeros(count)
			mylabels = []

			for idx, fam in enumerate(families_with_seats):
				mylabels.append(fam.name)
				y[idx] = fam.council

			plt.pie(y, labels = mylabels, startangle = 90, shadow = True)
			plt.title('Seats in City Council')
			plt.show() 