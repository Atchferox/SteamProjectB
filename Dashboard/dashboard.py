from tkinter import *
import json
from tkinter import ttk
from ctypes import windll

# Deze setting zorgt ervoor dat op elk soort display het dashboard scherp is
windll.shcore.SetProcessDpiAwareness(1)

bgcolor = "#222831"  # Achtergrond kleur
font_tuple = ("Montserrat Extra Light", 20)  # Font


with open('Dashboard/deelsteam.json', 'r') as f:
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


def getselectedelement(event):
    selection = event.widget.curselection()
    index = selection[0]
    value = event.widget.get(index)
    return value


def gamewindow():

    sortdictforgame = sorting_data(data)

    win = Toplevel()
    win.configure(bg=bgcolor)
    win.title("Library")
    win.state('zoomed')
    scrollbar = Scrollbar(win)

    scrollbar.pack(side=LEFT, fill='y')

    gamelijst = Listbox(win)
    gamelijst.pack(side=LEFT, padx=12, fill='y', pady=10)
    gamelijst.configure(font=("Montserrat Extra Light", 16), bg=bgcolor, fg='White',
                        activestyle='none', borderwidth=0, highlightthickness=0, selectbackground='#003A6E')
    # Als een item geselecteerd is dan word de functie gecalled
    gamelijst.bind('<<ListboxSelect>>', getselectedelement)

    i = 0
    len_max = 0
    for key, x in sortdictforgame:
        gamelijst.insert(i, key)
        i += 1
        if len(key) > len_max:
            len_max = len(key)

    gamelijst.config(yscrollcommand=scrollbar.set, width=len_max)
    scrollbar.config(command=gamelijst.yview, width=15, bg=bgcolor)


dashboardwindow = Tk()  # maakt het tkinter window

menubar = Menu()

dashboardwindow.title("Dashboard")  # Title van de window
dashboardwindow.state('zoomed')  # Fullscreen


# Standaard achtergrond kleur
dashboardwindow.configure(menu=menubar, background=bgcolor)

# Toont het eerste spel uit het bronbestand
label1 = Label(text=f"Het eerste spel is {eerstespel}")
label1.configure(font=(font_tuple), bg=bgcolor, fg='white')
label1.pack(pady=12)

# toont de gesorteerde dictionary van spellen op release datum
label2 = Label()
label2.configure(font=(font_tuple), bg=bgcolor, fg='white')
label2.pack()


steam_menu = Menu(menubar, tearoff=0)  # Maakt het steam menu
games_menu = Menu(menubar, tearoff=0)  # Maakt het games menu

games_menu.add_command(
    label='Library',
    command=gamewindow)

steam_menu.add_command(label="Friends")
steam_menu.add_separator()

steam_menu.add_command(
    label="Exit",
    command=dashboardwindow.destroy
)

menubar.add_cascade(
    label="Steam",
    menu=steam_menu
)

menubar.add_cascade(
    label="Games",
    menu=games_menu
)


if __name__ == '__main__':
    mainloop()
