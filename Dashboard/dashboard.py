from tkinter import *
import json

bgcolor = "#222831"  # Achtergrond kleur
font_tuple = ("Montserrat Extra Light", 20)  # Font


with open('Datasteam\deelsteam.json', 'r') as f:
    data = json.load(f)
    eerstespel = data[0]["name"]


def sorting_data(databestand):
    i = 0
    dic = {}
    while i < len(data):
        # Voegt de naam en de release date toe aan een dictionary
        dic[data[i]['name']] = data[i]['release_date']
        i += 1

    # Sorteert de dictionary aan de hand van de values
    sortdict = sorted(dic.items(), key=lambda x: x[1])
    return sortdict


dashboardwindow = Tk()  # maakt het tkinter window

dashboardwindow.title("Dashboard")  # Title van de window
dashboardwindow.state('zoomed')  # Fullscreen

# Standaard achtergrond kleur
dashboardwindow.configure(background=bgcolor)

label1 = Label(text=eerstespel)  # Toont het eerste spel uit het bronbestand
label1.configure(font=(font_tuple), bg=bgcolor, fg='white')
label1.pack()

# toont de gesorteerde dictionary van spellen op release datum
label2 = Label(text=sorting_data(data), wraplength=1000)
label2.configure(font=(font_tuple), bg=bgcolor, fg='white')
label2.pack()


mainloop()
