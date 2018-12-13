from tkinter import *
from tkinter.ttk import *
from main_beta import scrape_parish
from page_parsing import estimated_time

window = Tk()
window.title("City chooser")
selected = IntVar()
parish = {1:"tallinn", 2:"tartu", 3:"narva",4:"parnu"}

lbl = Label(window, text="Estimate time:").grid(column=0, row=1)
lbl = Label(window, text="------")
lbl.grid(column=4, row=1)

def clicked():
	city  = parish[selected.get()]
	print(city)
	time = estimated_time(city)
	lbl.configure(text=str(time)+' seconds')
	print(time)
	#scrape_parish(city)

rad1 = Radiobutton(window,text='Tallinn', value=1, variable=selected).grid(column=0, row=0)
rad2 = Radiobutton(window,text='Tartu', value=2, variable=selected).grid(column=1, row=0)
rad3 = Radiobutton(window,text='Narva', value=3, variable=selected).grid(column=2, row=0)
rad4 = Radiobutton(window,text='Parnu', value=4, variable=selected).grid(column=3, row=0)
btn = Button(window, text="Tap to download database", command=clicked).grid(column=4, row=0)
window.mainloop()
