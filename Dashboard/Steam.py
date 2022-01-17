import PySimpleGUI as sg
import json

sg.theme('darkgray10')
font = ("Montserrat Extra Light", 20)

with open('deelsteam.json', 'r') as f:
    data = json.load(f)
    eerstespel = data[0]["name"]


def dashboard():
    menu_def = [['Steam', ['Friends::friendskey', 'Help', 'About', '---', 'Contact Steam', '---', 'Exit::exitkey']],
                ['Library', ['Games::Gameskey']]
                ]  # Hier komen de menu opties in. ['menu'['alles wat in het menu komt']]
    layout = [
        [sg.Menu(menu_def)],
        [sg.Text(eerstespel, font=font)]
    ]

    return sg.Window('Dashboard', layout, finalize=True, resizable=True)


def Gamewindow():
    sortdictforgame = sorting_data(data)
    len_max = 0
    gamelijst = []
    for name, x in sortdictforgame:
        gamelijst.append(name)  # Insert de namen in de listbox

        # Dit maakt de lengte van de listbox. Word nog aangepast naar een functie die een scrollbar toevoegt als de namen lang zijn.
        if len(name) > len_max:
            len_max = len(name)

    layout2 = [
        [sg.Text('Dit is het gameswindow', font=font)],
        [sg.Listbox(
            values=gamelijst, size=(len_max, len(gamelijst)),
            font=font, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, key='listbox_g', enable_events=True)
         ]
    ]
    return sg.Window('Games', layout2, finalize=True, resizable=True)


dashboard, window2 = dashboard(), None


def sorting_data(data):
    i = 0
    dic = {}
    while i < len(data):
        # Voegt de naam en de release date toe aan een dictionary
        dic[data[i]['name']] = data[i]['release_date'], data[i]['appid']
        i += 1

    # Sorteert de dictionary aan de hand van de values
    sortdict = sorted(dic.items(), key=lambda x: x[1])
    return sortdict


while True:
    window, event, values = sg.read_all_windows()
    print(window, event, values)
    if event == sg.WIN_CLOSED or event == 'Exit::exitkey':
        window.close()

        if window == window2:
            window2 = None

        elif window == dashboard:
            break

    elif event == 'Games::Gameskey' and not window2:
        window2 = Gamewindow()

window.close()
