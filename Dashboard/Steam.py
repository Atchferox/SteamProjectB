
import PySimpleGUI as sg  # pip install PySimpleGUI
import json
from ctypes import windll
import requests
# Hierdoor is het op elk scherm high definition
windll.shcore.SetProcessDpiAwareness(1)

sg.theme('darkgray10')
font = ("Montserrat Extra Light", 20)  # test font

with open('deelsteam.json', 'r') as f:
    data = json.load(f)
    eerstespel = data[0]["name"]


def game_lijst():
    sortdic
    len_max = 0
    gamelijst = []
    for name in sortdic:
        gamelijst.append(name)  # Insert de namen in de listbox

        if len(name) > len_max:
            len_max = len(name)
    return gamelijst, len_max


def top100games():
    request = requests.get('https://steamspy.com/api.php?request=top100in2weeks')
    data = request.json()
    listofgames = []
    for key in data:
        listofgames.append(data[key]['name'])
    return listofgames


def dashboard():
    menu_def = [['Steam', ['Friends::friendskey', 'Help', 'About', '---', 'Contact Steam', '---', 'Exit::exitkey']],
                ['Library', ['Games::Gameskey']]
                ]  # Hier komen de menu opties in. ['menu'['alles wat in het menu komt']]
    layout = [
        [sg.Menu(menu_def)]
        
    ]

    return sg.Window('Dashboard', layout, finalize=True, resizable=True, icon='img/steamlogo.ico')


def Game_window():
    gamelijst, len_max = game_lijst()

    layout2 = [
        [sg.Text('Dit is de gameswindow', font=font)],
        [sg.Listbox(
            values=gamelijst, size=(len_max, len(gamelijst)),
            font=font, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, key='listbox_g', bind_return_key=True,
            enable_events=True)]]

    return sg.Window('Games', layout2, finalize=True, resizable=True, icon='img/steamlogo.ico')


def friend_window():
    layout3 = [[sg.Text('Friends', font=font)],
               [sg.Text('Search for friends')],
               [sg.Input(do_not_clear=False, key='-INPUT-'), sg.Button('Search')]]

    return sg.Window('Friends', layout3, finalize=True, resizable=True, icon='img/steamlogo.ico')


def sorting_data(data):
    i = 0
    dic = {}
    while i < len(data):
        # Voegt de naam en de app id toe aan een dictionary
        dic[data[i]['name']] = data[i]['appid']
        i += 1

    return dic


dashboard, window2, window3 = dashboard(), None, None


while True:
    window, event, values = sg.read_all_windows()

    if event == sg.WIN_CLOSED or event == 'Exit::exitkey':
        window.close()

        if window == window2:
            window2 = None

        elif window == window3:
            window3 = None

        elif window == dashboard:
            break

    elif event == 'Games::Gameskey' and not window2:  # Opent window 2
        sortdic = sorting_data(data)
        window2 = Game_window()

    elif event == 'listbox_g':  # Window 2
        name = values[event]
        keydic = name[0]
        app_id = sortdic[keydic]

    elif event == 'Friends::friendskey' and not window3:  # Opent window 3
        window3 = friend_window()

    elif event == 'Search':
        print(values['-INPUT-'])


window.close()
