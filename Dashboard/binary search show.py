from tkinter import *
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
from ctypes import windll

# Deze setting zorgt ervoor dat op elk soort display het dashboard scherp is
windll.shcore.SetProcessDpiAwareness(1)

bgcolor = "#222831"  # Achtergrond kleur
font_tuple = ("Montserrat Extra Light", 20)  # Font

with open('deelsteam.json', 'r') as f:
    data = json.load(f)
    eerstespel = data[0]["name"]


def sorting_data(databestand):
    i = 0
    dic = {}
    while i < len(data):
        # Voegt de naam en de release date toe aan een dictionary
        dic[data[i]['name']] = data[i]['release_date'], data[i]['appid']
        i += 1

    # Sorteert de dictionary aan de hand van de values
    sortdict = sorted(dic.items(), key=lambda x: x[1])
    return sortdict

def gamewindow():
    sortdictforgame = sorting_data(data)
    print(sortdictforgame)

    # Alfabetische lijst van spellen voor binary search
    alfa_gamelijst_unsorted = []
    for i in sortdictforgame:
        spelnaam = i[0].lower()
        alfa_gamelijst_unsorted.append(spelnaam)
    alfa_gamelijst_sorted = alfa_gamelijst_unsorted.copy()
    alfa_gamelijst_sorted.sort()

    dic_id = {}
    for i in sortdictforgame:
        naam = i[0]
        id = i[1][1]
        dic_id[naam] = id

    def binary_search():
        '''Binary search in spellen lijst'''
        gamelijst.selection_clear(0, 'end')
        left = 0
        right = len(alfa_gamelijst_sorted) - 1

        naamentry = searchbar.get()
        print(naamentry)

        while left <= right:
            avg = int(left + (right - left) / 2)

            if alfa_gamelijst_sorted[avg] == naamentry:
                print(f'naam gevonden: {alfa_gamelijst_sorted[avg]}')

                value = alfa_gamelijst_sorted[avg]
                list_index = alfa_gamelijst_unsorted.index(value)
                gamelijst.selection_set(list_index)

                for i in dic_id:
                    lower_case_value = i.lower()
                    if value == lower_case_value:
                        value = i
                        break
                    else:
                        continue

                produce_bar(value)
                break
            elif alfa_gamelijst_sorted[avg] < naamentry:
                left = left + 1
            elif alfa_gamelijst_sorted[avg] > naamentry:
                right = right - 1
        else:
            print('not found')
        return

    def produce_bar(value):
        '''Maakt een tabel voor het weergeven van het percentage van positieve / negatieve reviews'''
        try:  # Voor in het geval dat er nog geen diagram wordt getoond
            clear_figures()

        except NameError:
            pass

        appid = dic_id[value]

        request = requests.get(f'https://steamspy.com/api.php?request=appdetails&appid={appid}')
        apidata = request.json()

        names = ['Positive reviews', 'Negative reviews']
        values = [(apidata['positive'] / (apidata['positive'] + apidata['negative'])) * 100,
                  (apidata['negative'] / (apidata['positive'] + apidata['negative'])) * 100]

        review_bar = Figure(figsize=(5, 6), dpi=100)
        review_bar.add_subplot(111).bar(names, values)
        review_bar.suptitle('Reviews', color='white')
        review_bar.set_facecolor(bgcolor)

        global canvas
        canvas = FigureCanvasTkAgg(review_bar, librarywin)

        canvas.draw()

        canvas.get_tk_widget().pack(pady=100, side=LEFT, anchor=N)

    def clear_figures():
        '''Maakt de canvas van de staafdiagram leeg'''
        canvas.get_tk_widget().destroy()

    def getselectedelement(event):
        selection = event.widget.curselection()
        index = selection[0]
        value = event.widget.get(index)
        produce_bar(value)  # Diagrammen bij het geselecteerde spel worden opgehaald

    librarywin = Toplevel()  # Maakt top level window
    librarywin.configure(bg=bgcolor)
    librarywin.title("Library")
    librarywin.state('zoomed')
    scrollbar = Scrollbar(librarywin)  # Voegt een scrollbar toe

    scrollbar.pack(side=LEFT, fill='y')

    gamelijst = Listbox(librarywin)
    gamelijst.pack(side=LEFT, padx=12, fill='y', pady=10)
    gamelijst.configure(font=("Montserrat Extra Light", 16), bg=bgcolor, fg='White',
                        activestyle='none', borderwidth=0, highlightthickness=0, selectbackground='#003A6E')
    # Als een item geselecteerd is dan word de functie gecalled
    gamelijst.bind('<<ListboxSelect>>', getselectedelement)  # Als een item word geselecteerd

    searchbar = Entry(librarywin)
    searchbar.pack(side=TOP)

    searchbutton = Button(librarywin, text='Zoek')
    searchbutton.config(command=binary_search)
    searchbutton.pack(side=TOP)

    i = 0
    len_max = 0
    for key, x in sortdictforgame:
        gamelijst.insert(i, key)  # Insert de namen in de listbox
        i += 1
        # Dit maakt de lengte van de listbox. Word nog aangepast naar een functie die een scrollbar toevoegt als de namen lang zijn.
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
