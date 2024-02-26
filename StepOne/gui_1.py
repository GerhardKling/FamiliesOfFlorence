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

#Labels
label_frm = tk.Label(frm, text = "Hello World!")
label_frm.grid(column = 0, row = 0)

#Buttons
button_frm = tk.Button(frm, text = "Exit", command = root.destroy)
button_frm.grid(column = 1, row = 0)

#Mainloop at the end
root.mainloop()

