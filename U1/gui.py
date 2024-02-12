"""
Builds GUI
"""
import tkinter as tk
from tkinter import messagebox, simpledialog
import pickle
import numpy as np
import random

from player import Player
from family import Family
from game import Game
from weather import Weather
from price import Price
from spouse import Spouse
from names import Names
from children import Children

#Root
root = tk.Tk()
root.title('Families of Florence')

#Size of widget
root.geometry("1000x1100")

#Icon: ico file 16 by 16
root.iconbitmap('Globe.ico')

"""
Functions for menus amd buttons
"""
def donothing():
   filewin = tk.Toplevel(root)
   button = tk.Button(filewin, text="Do nothing button")
   button.pack()


def start_button_function():
	"""Function for start button"""
	#Get first and last name from entry widget
	f_name_get = f_name.get()
	l_name_get = l_name.get()

	#Get gender
	gender_get = gender.get()

	#Create global variables
	global player
	global family
	global game
	global price

	#Initialize person
	player = Player(name = f_name_get, gender = gender_get)

	#Start family
	family = Family(name = l_name_get)

	# #Add player to family
	# family.add_player_to_family(player)

	#Add player to Game
	game = Game()
	game.add_player(player)

	#Add other families to game
	game.start_other_families()

	#Initialize prices
	price = Price()

	#Close new_game_window
	new_game_window.destroy()


def new_game():
    #New window
    global new_game_window
    new_game_window = tk.Toplevel()
    new_game_window.title('New Game')
    
    #Size of widget
    new_game_window.geometry("400x300")
    
    #Icon: ico file 16 by 16
    new_game_window.iconbitmap('Globe.ico')	

    #Create global variables
    global f_name
    global l_name
    global gender

    f_name = tk.StringVar() 
    l_name = tk.StringVar() 

    #Entry: first and last name
    f_name_entry = tk.Entry(new_game_window, width = 30, textvariable = f_name)
    f_name_entry.grid(row = 0, column = 1, padx = 20)  
     
    l_name_entry = tk.Entry(new_game_window, width = 30, textvariable = l_name)
    l_name_entry.grid(row = 1, column = 1, padx = 20) 

    #Labels for entry
    f_name_label = tk.Label(new_game_window, text = "First name")
    f_name_label.grid(row = 0, column = 0)
    
    l_name_label = tk.Label(new_game_window, text = "Last name")
    l_name_label.grid(row = 1, column = 0)   

    #Radio button
    gender = tk.IntVar()
    gender.set('1')

    #Options for radio button as list of tuples
    OPTIONS = [('Male', '0'), ('Female', '1')]

    for option in OPTIONS:
    	radio_button = tk.Radiobutton(new_game_window, text = option[0], variable = gender, \
    	value = option[1])
    	radio_button.grid(row = int(option[1]) + 2, column = 1)

	#Create start button
    start_button = tk.Button(new_game_window, text = "Start", command = start_button_function)
    start_button.grid(row = 4, column = 1, columnspan = 2, \
    ipadx = 115, padx = 10, pady = 1)  


def save_game():
	"""Saves objects; overwrites any existing file; default game file 'game.pkl'"""
	obj = [player, family, game, weather, price]
	with open('game.pkl', 'wb') as output:
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_game():
	"""Loads objects; default game file"""
	with open('game.pkl', 'rb') as input:
		obj = pickle.load(input)
	global player, family, game, weather, price
	player = obj[0]
	family = obj[1]
	game = obj[2]
	weather = obj[3]
	price = obj[4]


def next_year():
	#Weather and prices in the year
	global weather
	global player

	#Start weather
	weather = Weather()

	#Adjust land prices
	price.change_land_price(game, player)
	#Adjust grain prices
	price.change_grain_prices(weather)
	#Adjust interest rates
	price.change_interest_rates()

	#Add one year
	game.year += 1

	#Names
	names = Names()

	#Aging of players & checking whether alive
	for player in game.players:
		player.age += 1
		player.check_alive()

	#Aging of family members
	for fam in family.members:
		fam.age += 1
		fam.check_alive()
		if not fam.alive:
			tk.messagebox.showwarning(title = 'Death in Family', message = f'Sadly {fam.name} died at age {fam.age}.')
			if not fam.inherit: #Death of spouse
				player.spouse = False
				#Remove display for spouse
				name_spouse_display.delete(0, "end")
			family.members.remove(fam)
			del fam

	#Aging of members of extended family
	for fam in family.extended:
		fam.age += 1
		fam.check_alive()
		if not fam.alive:
			family.extended.remove(fam)
			del fam

	#Add previous Head to family history
	if player.alive == False:
		#Tuple with main statistics
		stats = (family.title[player.gender], player.name, family.name, player.age, game.year)
		family.history.append(stats)

		#Start next Head
		#Look for heir in family; sort by age
		family.members.sort(key = lambda x: x.age)
		heirs = [fam for fam in family.members if fam.inherit]

		#No child & spouse
		if len(heirs) == 0 and len(family.members) == 0:
			tk.messagebox.showwarning(title = 'No Heir', message = 'You do not have any heir. Loss of title & land.')
			player.owner = []
			player.cash = 0.20 * player.cash
			family.title = ('Mr', 'Mrs', 0)
			player.age = random.randint(14, 20)
			player.gender = random.randint(0, 1)
			player.alive = True
			player.spouse = False
			if player.gender == 0:
				player.name = names.male_name[random.randint(0, len(names.male_name) - 1)]
			else:
				player.name = names.female_name[random.randint(0, len(names.female_name) - 1)]
			#Remove display for spouse
			name_spouse_display.delete(0, "end")
		#Only spouse
		if len(heirs) == 0 and len(family.members) == 1:
			tk.messagebox.showinfo(title = 'Spouse inherits', message = 'Your spouse inherits title & land.')
			player.name = family.members[0].name
			player.age = family.members[0].age
			player.gender = family.members[0].gender
			player.alive = True
			player.spouse = False
			#Remove spouse from family members
			family.members = []
			#Remove display for spouse
			name_spouse_display.delete(0, "end")

		if len(heirs) > 0:
			tk.messagebox.showinfo(title = 'Inheritance', message = f'{heirs[-1].name} inherits title & land.')
			player.name = heirs[-1].name
			player.age = heirs[-1].age
			player.gender = heirs[-1].gender
			player.alive = True
			player.spouse = False
			#Remove all other children and spouse of previous Head; move to extended family
			family.extended.extend(family.members)
			family.members = []
			#Remove display for spouse
			name_spouse_display.delete(0, "end")

	#Growth of extended family
	for _ in range(len(family.extended)):
		prob = random.uniform(0, 1)
		if prob < 0.03:
			child = Children(name = "TBA", gender = random.randint(0, 1))
			if child.gender == 0:
				child.name = names.male_name[random.randint(0, len(names.male_name) - 1)]
				child_gender = 'son'
			else:
				child.name = names.female_name[random.randint(0, len(names.female_name) - 1)]
				child_gender = 'daughter '
			#Add child to family
			family.extended.append(child)


	#Profits from farms etc. & wealth
	farm_profits = 0
	count = 0
	player.wealth = 0
	for player in game.players:
		if player.owner:
			for farm in player.owner:
				farm_profits += farm.profit(weather.outcome, price.grain)
				player.cash += farm.profit(weather.outcome, price.grain)
				count += 1
				player.wealth += price.land * 10

	#Pay interest on debt
	interest_payment = player.debt * price.interest
	player.cash -= interest_payment

	#Profits from manufactoring
	other_profits = 0
	#Check the number of farms
	if len(player.owner) < 5 * player.mill:
		other_profits = 0
		tk.messagebox.showwarning(title = 'No Supplies', message = 'Not enough farms for your mills.')
	elif player.mill > 0 and player.bakery == 0 and player.brewery == 0:
		other_profits = 0
		tk.messagebox.showwarning(title = 'No Workshops', message = 'No workshops for mills.')
	else:
		min_price = max(price.grain, 0.3)
		other_profits = 200 * weather.outcome * player.bakery * min_price * 1.2 + 250 * weather.outcome * player.brewery * min_price * 1.5

	#Add profits to player
	player.cash += other_profits

	#Take loan if negative cash
	if player.cash < 0:
		player.debt += -player.cash
		player.cash = 0

	#Adjust wealth for cash and debt
	player.wealth += player.cash - player.debt

	#Adjust wealth for mills and workshops
	player.wealth += 100 * player.mill + 150 * player.bakery + 250 * player.brewery

	#Check whether player is bankrupt
	if player.wealth < 0:
		tk.messagebox.showwarning(title = 'Bankrupt', message = 'The bank liquidates your assets & title.')
		player.owner = [] #All farms liquidated
		player.cash = 50
		player.debt = 0
		family.title = ('Mr', 'Mrs', 0)

	#Adjust wealth on family
	family.wealth = player.wealth

	#Report financial position
	cash_display.delete(0, "end")
	cash_display.insert(0, int(player.cash))

	debt_display.delete(0, "end")
	debt_display.insert(0, int(player.debt))

	interest_payment_display.delete(0, "end")
	interest_payment_display.insert(0, int(interest_payment))

	profit_display.delete(0, "end")
	profit_display.insert(0, int(farm_profits))	

	other_profit_display.delete(0, "end")
	other_profit_display.insert(0, int(other_profits))	

	farm_display.delete(0, "end")
	farm_display.insert(0, count)	

	mill_display.delete(0, "end")
	mill_display.insert(0, player.mill)		

	bakery_display.delete(0, "end")
	bakery_display.insert(0, player.bakery)	

	brewery_display.delete(0, "end")
	brewery_display.insert(0, player.brewery)	

	wealth_display.delete(0, "end")
	wealth_display.insert(0, int(player.wealth))	

	#Report weather and prices
	weather_display.delete(0, "end")
	weather_display.insert(0, weather.weather)

	land_price_display.delete(0, "end")
	land_price_display.insert(0, round(price.land, 1))

	grain_price_display.delete(0, "end")
	grain_price_display.insert(0, round(price.grain, 2))	

	interest_display.delete(0, "end")
	interest_display.insert(0, f"{round(price.interest * 100, 1)} %")	

	#Report about the family	
	#Head of family
	name_display.delete(0, "end")
	name_display.insert(0, f"{family.title[player.gender]} {player.name} {family.name} is {player.age} old.")
	#Spouse
	if player.spouse:
		name_spouse_display.delete(0, "end")
		#Sort family members by age
		find_spouse = [fam for fam in family.members if not fam.inherit]
		name_spouse_display.insert(0, f"{find_spouse[0].name} is {find_spouse[0].age} old.")	
	#Children
	children_display = ''
	family.members.sort(key = lambda x: x.age)
	children = [child for child in family.members if child.inherit]
	for child in children:
		children_display += child.name + ', '

	name_children_display.delete(0, "end")	
	name_children_display.insert(0, children_display)

	num_family_display.delete(0, "end")
	num_family_display.insert(0, f"{len(family.extended) + len(family.members) + 1}")

	#Report about the family history
	for idx, history in enumerate(family.history):
		previous_name_display = tk.Entry(family_history_frame, width = 60, borderwidth = 5)
		previous_name_display.grid(row = idx + 1, column = 1)
		tk.Label(family_history_frame, text = "Tile & Name").grid(row = idx + 1, column = 0)	
		previous_name_display.delete(0, "end")
		previous_name_display.insert(0, f"{history[0]} {history[1]} {history[2]} dies at age {history[3]}: {history[4] - history[3]} - {history[4]}.")

	#Marriage proposal
	#Names for spouse
	for fam in game.other_families:
		prob = random.uniform(0, 1)
		if player.spouse == False and fam.title[2] <= family.title[2] + 1 and fam.farm <= count + 4 and player.age > 16 and prob < 0.3:
			spouse = Spouse(name = "TBA", gender = (player.gender + 1) % 2, age = random.randint(18, 25))
			if spouse.gender == 0:
				spouse.name = names.male_name[random.randint(0, len(names.male_name) - 1)]
			else:
				spouse.name = names.female_name[random.randint(0, len(names.female_name) - 1)]

			proposal = tk.messagebox.askquestion('Marriage Proposal', \
			f'Do you want to mary {fam.title[spouse.gender]} {spouse.name} {fam.name} who is {spouse.age} years old.')
			if proposal == 'yes':
				#Get married
				player.spouse = True
				#Add spouse to family & reject all other proposals
				family.add_player_to_family(spouse)
				#Adjust family title if better
				if fam.title[2] > family.title[2]:
					family.title = fam.title
				elif fam.title[2] <= family.title[2]:
					support = random.randint(50, 150)
					player.cash += support
					tk.messagebox.showinfo(title = 'Family Support', message = f'{fam.name} provides financial support of {support}.')
				break

	#Children
	if player.spouse and player.age < 50:
		prob = random.uniform(0, 1)
		if prob < 0.15:
			child = Children(name = "TBA", gender = random.randint(0, 1))
			if child.gender == 0:
				child.name = names.male_name[random.randint(0, len(names.male_name) - 1)]
				child_gender = 'son'
			else:
				child.name = names.female_name[random.randint(0, len(names.female_name) - 1)]
				child_gender = 'daughter '
			#Add child to family
			family.add_player_to_family(child)
			#Announcement
			tk.messagebox.showinfo(title = 'New Family Member', message = f'Your {child_gender} {child.name} was born.')

	#Elections
	game.election(family, price.land)


def buy_farm():
	"""Buys farms"""
	owned_land = 0
	for fam in game.other_families:
		owned_land += fam.farm		
	#Add ownership of player
	owned_land += len(player.owner)
	#Determine maximum number of farms available
	max_farms = game.total_farm - owned_land
	num_farms = simpledialog.askinteger(f"One farm costs {int(10 * price.land)}.", "How many farms do you want to buy?", parent = root)
	if num_farms > max_farms:
		num_farms = max_farms
		tk.messagebox.showwarning(title = 'Warning', message = f'There are only {max_farms} farms on the market.')
	count = 0
	for _ in range(num_farms):
		can_buy = player.buy_farm(land = 10, price_land = price.land)
		if can_buy:
			count += 1
	if count == 0 and max_farms != 0:
		tk.messagebox.showwarning(title = 'Warning', message = 'Not enough funds for one farm.')
	else:
		tk.messagebox.showinfo(title = 'Purchase of Farm', message = f'You bought {count} farm.')


def sell_farm():
	"""Sells farms"""
	num_farms = simpledialog.askinteger(f"You own {len(player.owner)} farms and {player.mill} mills.", "How many farms do you want to sell?", parent = root)
	if num_farms > len(player.owner):
		num_farms = len(player.owner)
	for _ in range(num_farms):
		player.sell_farm(price_land = price.land)
	tk.messagebox.showinfo(title = 'Sale of Farm', message = f'You sold {num_farms} farms.')


def take_loan_function():
	"""Function for take button; takes more loans"""
	#Get loan amount
	take_loan_get = take_loan.get()
	#Add loan to player's debt; convert to integer
	player.debt += int(take_loan_get)
	player.cash += int(take_loan_get)
	#Close bank window
	bank_window.destroy()
	#Show message
	tk.messagebox.showinfo(title = 'Message from Bank', message = f'You took a {int(take_loan_get)} loan.')


def repay_loan_function():
	"""Function for repay button; repays loans"""
	#Get loan amount
	repay_loan_get = repay_loan.get()
	#Reduce player's debt; convert to integer
	player.debt -= int(repay_loan_get)
	player.cash -= int(repay_loan_get)
	#Close bank window
	bank_window.destroy()
	#Show message
	tk.messagebox.showinfo(title = 'Message from Bank', message = f'You repaid {int(repay_loan_get)} of your debt.')	


def loan():
	"""Take and repay loans"""
	#New window
	global bank_window
	bank_window = tk.Toplevel()
	bank_window.title('At the Bank')

	#Size of widget
	bank_window.geometry("400x300")

	#Icon: ico file 16 by 16
	bank_window.iconbitmap('Globe.ico')	

	#Create global variables
	global take_loan
	global repay_loan

	#Maximum loan amount
	max_loan = (family.title[2] + 1) * 100 + (len(player.owner) * 10 * price.land + player.cash) * 0.8 - player.debt

	#Adjust if debt capacity is reached
	if max_loan < 0:
		max_loan = 0

	#Maximum repayment
	if player.debt >= player.cash:
		max_repay = player.cash
	else:
		max_repay = player.debt

	tk.Label(bank_window, text = "Select Additional Loan").grid(row = 0, column = 0, columnspan = 2)
	take_loan = tk.Scale(bank_window, from_ = 0, to = max_loan, orient = tk.HORIZONTAL)
	take_loan.grid(row = 1, column = 0)
	take_loan.set('0')

	tk.Label(bank_window, text = "Repay Loans").grid(row = 2, column = 0, columnspan = 2)
	repay_loan = tk.Scale(bank_window, from_ = 0, to = max_repay, orient = tk.HORIZONTAL)
	repay_loan.grid(row = 3, column = 0)
	repay_loan.set('0')

	#Create start button
	take_button = tk.Button(bank_window, text = "Take loan", command = take_loan_function)
	take_button.grid(row = 4, column = 0, ipadx = 115, padx = 10, pady = 1)  

	repay_button = tk.Button(bank_window, text = "Repay loan", command = repay_loan_function)
	repay_button.grid(row = 5, column = 0, ipadx = 115, padx = 10, pady = 1)  


def join_bakers():
	"""Join bakers guild"""
	answer = tk.messagebox.askquestion('Join Guild', 'Do you want to join the Bakers Guild for 100?')
	if answer == 'yes':
		if player.cash >= 100:
			player.cash -= 100
			family.guilds.append('Bakers')
		else:
			tk.messagebox.showwarning(title = 'Warning', message = 'Not enough cash.')


def join_brewers():
	"""Join brewers guild"""
	answer = tk.messagebox.askquestion('Join Guild', 'Do you want to join the Brewers Guild for 200?')
	if answer == 'yes':
		if player.cash >= 200:
			player.cash -= 200
			family.guilds.append('Brewers')
		else:
			tk.messagebox.showwarning(title = 'Warning', message = 'Not enough cash.')


def buy_mill():
	"""Buys one mill, which needs 5 farms"""
	answer = tk.messagebox.askquestion('Buy Mill', 'Do you want to buy a mill for 100?')
	if len(player.owner) - player.mill * 5 < 5 and answer == 'yes':
		tk.messagebox.showwarning(title = 'Warning', message = 'You need 5 farms to support the mill.')
	elif answer == 'yes':
		if player.cash >= 100:
			player.cash -= 100
			player.mill += 1
		else:
			tk.messagebox.showwarning(title = 'Warning', message = 'Not enough cash.')


def buy_bakery():
	"""Buys one bakery, one mill supports one bakery"""
	answer = tk.messagebox.askquestion('Buy Bakery', 'Do you want to buy a bakery for 150?')
	if 'Bakers' not in family.guilds and answer == 'yes':
		tk.messagebox.showwarning(title = 'Warning', message = 'You need to join the Bakers Guild first.')
	elif player.mill - player.bakery - player.brewery == 0 and answer == 'yes':
		tk.messagebox.showwarning(title = 'Warning', message = 'You need 1 mill to support the bakery.')
	elif answer == 'yes':
		if player.cash >= 150:
			player.cash -= 150
			player.bakery += 1
		else:
			tk.messagebox.showwarning(title = 'Warning', message = 'Not enough cash.')


def buy_brewery():
	"""Buys one brewery, one mill supports one brewery"""
	answer = tk.messagebox.askquestion('Buy Brewery', 'Do you want to buy a brewery for 250?')
	if 'Brewers' not in family.guilds and answer == 'yes':
		tk.messagebox.showwarning(title = 'Warning', message = 'You need to join the Brewers Guild first.')
	elif player.mill - player.bakery - player.brewery == 0 and answer == 'yes':
		tk.messagebox.showwarning(title = 'Warning', message = 'You need 1 mill to support the bakery.')
	elif answer == 'yes':
		if player.cash >= 250:
			player.cash -= 250
			player.brewery += 1
		else:
			tk.messagebox.showwarning(title = 'Warning', message = 'Not enough cash.')

"""
Menu bar   
"""
menubar = tk.Menu(root)

#File menu
file_menu = tk.Menu(menubar, tearoff = 0)
file_menu.add_command(label = "New", command = new_game)
file_menu.add_command(label = "Save", command = save_game)
file_menu.add_command(label = "Load", command = load_game)
file_menu.add_separator()
file_menu.add_command(label = "Exit", command = root.destroy)
menubar.add_cascade(label = "File", menu = file_menu)

#Invest menu
invest_menu = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "Invest", menu = invest_menu)

#Adds submenu to Buying: Farm, Mills
buy_sub_menu = tk.Menu(menubar, tearoff = 0)
buy_sub_menu.add_command(label = "Farm", command = buy_farm)
buy_sub_menu.add_command(label = "Mill", command = buy_mill)
buy_sub_menu.add_command(label = "Bakery", command = buy_bakery)
buy_sub_menu.add_command(label = "Brewery", command = buy_brewery)
invest_menu.add_cascade(label = "Buy", menu = buy_sub_menu)

#Adds submenu to Selling: Farm
sell_sub_menu = tk.Menu(menubar, tearoff = 0)
sell_sub_menu.add_command(label = "Farm", command = sell_farm)
sell_sub_menu.add_command(label = "Mill", command = donothing)
sell_sub_menu.add_command(label = "Bakery", command = donothing)
sell_sub_menu.add_command(label = "Brewery", command = donothing)
invest_menu.add_cascade(label = "Sell", menu = sell_sub_menu)


#Bank menu
bank_menu = tk.Menu(menubar, tearoff = 0)
bank_menu.add_command(label = "Loan", command = loan)
bank_menu.add_command(label = "Deposit", command = donothing)
menubar.add_cascade(label = "Bank", menu = bank_menu)


#Guilds menu
guilds_menu = tk.Menu(menubar, tearoff = 0)
guilds_menu.add_command(label = "Bakers", command = join_bakers)
guilds_menu.add_command(label = "Brewers", command = join_brewers)
menubar.add_cascade(label = "Guilds", menu = guilds_menu)


#Root configuration for menu bar
root.config(menu = menubar)


"""
Frame
"""
"""
Control frame: provides basic controls
"""
control_frame = tk.LabelFrame(root, text = 'Control')
control_frame.grid(row = 0, column = 0, \
sticky='W', padx = 5, pady = 20, ipadx = 40, ipady = 50)

#Buttons on control frame
next_button = tk.Button(control_frame, text = "Next", command = next_year)
next_button.grid(row = 0, column = 0)

"""
Current year frame: provides basic information
"""
current_frame = tk.LabelFrame(root, text = 'Current Year')
current_frame.grid(row = 0, column = 1, \
sticky='W', padx = 5, pady = 10, ipadx = 100, ipady = 30)

#Financial position display
fin_position_label = tk.Label(current_frame, text = "Financial Position").grid(row = 0, column = 0)
cash_display = tk.Entry(current_frame, width = 10, borderwidth = 5)
cash_display.grid(row = 1, column = 1)
cash_label = tk.Label(current_frame, text = "Cash position").grid(row = 1, column = 0)

debt_display = tk.Entry(current_frame, width = 10, borderwidth = 5)
debt_display.grid(row = 2, column = 1)
debt_label = tk.Label(current_frame, text = "Debt").grid(row = 2, column = 0)

interest_payment_display = tk.Entry(current_frame, width = 10, borderwidth = 5)
interest_payment_display.grid(row = 3, column = 1)
interest_payment_display_label = tk.Label(current_frame, text = "Interest payment").grid(row = 3, column = 0)

profit_display = tk.Entry(current_frame, width = 10, borderwidth = 5)
profit_display.grid(row = 4, column = 1)
profit_label = tk.Label(current_frame, text = "Profits from farms").grid(row = 4, column = 0)

other_profit_display = tk.Entry(current_frame, width = 10, borderwidth = 5)
other_profit_display.grid(row = 5, column = 1)
other_profit_label = tk.Label(current_frame, text = "Profits from manufacturing").grid(row = 5, column = 0)

farm_display = tk.Entry(current_frame, width = 10, borderwidth = 5)
farm_display.grid(row = 6, column = 1)
farm_label = tk.Label(current_frame, text = "Number of farms").grid(row = 6, column = 0)

mill_display = tk.Entry(current_frame, width = 10, borderwidth = 5)
mill_display.grid(row = 7, column = 1)
mill_label = tk.Label(current_frame, text = "Number of mills").grid(row = 7, column = 0)

bakery_display = tk.Entry(current_frame, width = 10, borderwidth = 5)
bakery_display.grid(row = 8, column = 1)
bakery_label = tk.Label(current_frame, text = "Number of bakeries").grid(row = 8, column = 0)

brewery_display = tk.Entry(current_frame, width = 10, borderwidth = 5)
brewery_display.grid(row = 9, column = 1)
brewery_label = tk.Label(current_frame, text = "Number of breweries").grid(row = 9, column = 0)

wealth_display = tk.Entry(current_frame, width = 10, borderwidth = 5)
wealth_display.grid(row = 10, column = 1)
wealth_label = tk.Label(current_frame, text = "Wealth").grid(row = 10, column = 0)

#Report weather and prices display: 
weather_prices_label = tk.Label(current_frame, text = "Weather & Prices").grid(row = 0, column = 3)
weather_display = tk.Entry(current_frame, width = 10, borderwidth = 5)
weather_display.grid(row = 1, column = 4)
weather_label = tk.Label(current_frame, text = "The weather was").grid(row = 1, column = 3)

land_price_display = tk.Entry(current_frame, width = 10, borderwidth = 5)
land_price_display.grid(row = 2, column = 4)
land_price_label = tk.Label(current_frame, text = "Price of land").grid(row = 2, column = 3)

grain_price_display = tk.Entry(current_frame, width = 10, borderwidth = 5)
grain_price_display.grid(row = 3, column = 4)
grain_price_label = tk.Label(current_frame, text = "Price of grain").grid(row = 3, column = 3)

interest_display = tk.Entry(current_frame, width = 10, borderwidth = 5)
interest_display.grid(row = 4, column = 4)
interest_label = tk.Label(current_frame, text = "Interest rate").grid(row = 4, column = 3)


"""
Family frame: provides information about the family
"""
family_frame = tk.LabelFrame(root, text = 'Your Family')
family_frame.grid(row = 1, column = 1, \
sticky='W', padx = 5, pady = 10, ipadx = 100, ipady = 30)

tk.Label(family_frame, text = "Head of the Family").grid(row = 0, column = 0)
name_display = tk.Entry(family_frame, width = 30, borderwidth = 5)
name_display.grid(row = 1, column = 1, sticky='W')
name_label = tk.Label(family_frame, text = "Tile & Name").grid(row = 1, column = 0, sticky='W')

tk.Label(family_frame, text = "Spouse & Children").grid(row = 2, column = 0)
name_spouse_display = tk.Entry(family_frame, width = 30, borderwidth = 5)
name_spouse_display.grid(row = 3, column = 1, sticky='W')
name_spouse_label = tk.Label(family_frame, text = "Spouse").grid(row = 3, column = 0, sticky='W')

name_children_display = tk.Entry(family_frame, width = 60, borderwidth = 5)
name_children_display.grid(row = 4, column = 1, sticky='W')
name_children_label = tk.Label(family_frame, text = "Children").grid(row = 4, column = 0, sticky='W')

num_family_display = tk.Entry(family_frame, width = 30, borderwidth = 5)
num_family_display.grid(row = 5, column = 1, sticky='W')
tk.Label(family_frame, text = "Family members").grid(row = 5, column = 0, sticky='W')

"""
Family history frame: provides information about the family history
"""
family_history_frame = tk.LabelFrame(root, text = 'Your Family History')
family_history_frame.grid(row = 2, column = 1, \
sticky='W', padx = 5, pady = 20, ipadx = 100, ipady = 100)

#See next_year function for dynamic display of family history
tk.Label(family_history_frame, text = "Previous Heads").grid(row = 0, column = 0)




#Running the loop
root.mainloop()