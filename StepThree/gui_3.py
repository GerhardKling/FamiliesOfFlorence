"""
Builds GUI
"""

import tkinter as tk

#Starts root
root = tk.Tk()
root.title('Families of Florence')

#Size
root.geometry("500x600")

#Frames
frm = tk.Frame(root)
frm.grid(column = 0, row = 0)

"""
Functions for buttons
"""
def do_nothing():
	print("Do nothing!")


def start_button_function():
	"""Function for start button"""
	#Get first and last name from entry widget
	f_name_get = f_name.get()
	l_name_get = l_name.get()

	#Get gender
	gender_get = gender.get()

	#Close new_game_window
	new_game_window.destroy()

	#CHECK
	print(f"{f_name_get} {l_name_get} is a {gender_get}.")


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

"""
Menu bar   
"""
menubar = tk.Menu(root)

#File menu
file_menu = tk.Menu(menubar, tearoff = 0)
file_menu.add_command(label = "New", command = new_game)
file_menu.add_command(label = "Save", command = do_nothing)
file_menu.add_command(label = "Load", command = do_nothing)
file_menu.add_separator()
file_menu.add_command(label = "Exit", command = root.destroy)
menubar.add_cascade(label = "File", menu = file_menu)

#Invest menu
invest_menu = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "Invest", menu = invest_menu)

#Adds submenu to Buying: Farm, Mills
buy_sub_menu = tk.Menu(menubar, tearoff = 0)
buy_sub_menu.add_command(label = "Farm", command = do_nothing)
buy_sub_menu.add_command(label = "Mill", command = do_nothing)
buy_sub_menu.add_command(label = "Bakery", command = do_nothing)
buy_sub_menu.add_command(label = "Brewery", command = do_nothing)
invest_menu.add_cascade(label = "Buy", menu = buy_sub_menu)

#Adds submenu to Selling: Farm
sell_sub_menu = tk.Menu(menubar, tearoff = 0)
sell_sub_menu.add_command(label = "Farm", command = do_nothing)
sell_sub_menu.add_command(label = "Mill", command = do_nothing)
sell_sub_menu.add_command(label = "Bakery", command = do_nothing)
sell_sub_menu.add_command(label = "Brewery", command = do_nothing)
invest_menu.add_cascade(label = "Sell", menu = sell_sub_menu)


#Bank menu
bank_menu = tk.Menu(menubar, tearoff = 0)
bank_menu.add_command(label = "Loan", command = do_nothing)
bank_menu.add_command(label = "Deposit", command = do_nothing)
menubar.add_cascade(label = "Bank", menu = bank_menu)


#Guilds menu
guilds_menu = tk.Menu(menubar, tearoff = 0)
guilds_menu.add_command(label = "Bakers", command = do_nothing)
guilds_menu.add_command(label = "Brewers", command = do_nothing)
menubar.add_cascade(label = "Guilds", menu = guilds_menu)

#Root configuration for menu bar
root.config(menu = menubar)

#Mainloop at the end
root.mainloop()

