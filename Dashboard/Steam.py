
import PySimpleGUI as sg  # pip install PySimpleGUI
import json
from ctypes import windll
import requests
# Hierdoor is het op elk scherm high definition
windll.shcore.SetProcessDpiAwareness(1)

sg.theme('darkgray10')
font = ("Montserrat Extra Light", 20)  # test font
font2 = ("Montserrat Extra Light", 14)



'''def game_lijst():
    sortdic = sorting_data(data)
    len_max = 0
    gamelijst = []
    for name in sortdic:
        gamelijst.append(name)  # Insert de namen in de listbox

        if len(name) > len_max:
            len_max = len(name)
    return gamelijst, len_max''' 


def dashboard():
    topgames, max_len = top100games()

    menu_def = [['Steam', ['Friends::friendskey', 'Help::help', 'About', '---', 'Contact Steam', '---', 'Exit::exitkey']],
                ['Library', ['Games::Gameskey']]]  # Hier komen de menu opties in. ['menu'['alles wat in het menu komt']]
    layout = [
        [sg.Menu(menu_def)],
        [sg.Text('Top 100 Games van de afgelopen 2 weken', font=font)],
        [sg.Listbox(
            values=topgames, size=(max_len, len(topgames)), font=font2,
            select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, key='listbox_t', bind_return_key=True,
            enable_events=True)]
    ]

    return sg.Window('Dashboard', layout, finalize=True, resizable=True, icon='img/steamlogo.ico')


def Game_window():

    layout2 = [
        [sg.Text('Jouw Games', font=font)],
        [sg.Text('Deze functie is nog in ontwikkeling')]]

    return sg.Window('Games', layout2, finalize=True, resizable=True, icon='img/steamlogo.ico')


def friend_window():
    layout3 = [[sg.Text('Vriendenlijst', font=font)],
               [sg.Text('Vul hier je steamID in om je vriendelijst te krijgen')],
               [sg.Input(do_not_clear=False, key='-INPUT-'),
                sg.Button('Search')],
               [sg.Text(key='-OUTPUT-')]
               ]

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
    elif event == 'Help::help':
        sg.Popup('Contact me: Luuk.Munneke@student.hu.nl', title='Help')

    elif event == 'Games::Gameskey' and not window2:  # Opent window 2
        window2 = Game_window()

    elif event == 'listbox_g':  # Window 2
        name = values[event]
        keydic = name[0]

    elif event == 'Friends::friendskey' and not window3:  # Opent window 3
        window3 = friend_window()

    elif event == 'Search':

        if not values['-INPUT-']:
            window['-OUTPUT-'].update(f"Results: \nName not found")
        else:
            steamid = get_steamid(values['-INPUT-'])

            window['-OUTPUT-'].update(f"Results: \n{values['-INPUT-']}")


window.close()
