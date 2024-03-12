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

# #Labels
# label_frm = tk.Label(frm, text = "Hello World!")
# label_frm.grid(column = 0, row = 0)

# #Buttons
# button_frm = tk.Button(frm, text = "Exit", command = root.destroy)
# button_frm.grid(column = 1, row = 0)


"""
Functions for buttons
"""
def do_nothing():
	print("Do nothing!")


"""
Menu bar   
"""
menubar = tk.Menu(root)

#File menu
file_menu = tk.Menu(menubar, tearoff = 0)
file_menu.add_command(label = "New", command = do_nothing)
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

