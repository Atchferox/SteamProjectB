from tokenize import Name
from xml.dom.minidom import Attr
import PySimpleGUI as sg  # pip install PySimpleGUI
from ctypes import windll
from API.API import *

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


def friend_list_window():
    layout3 = [
        [sg.Text('Vriendenlijst', font=font)],
        [sg.Text('Vul hier je steamID in om je vriendelijst te krijgen')],
        [sg.Input(do_not_clear=False, key='-INPUT-'),
         sg.Button('Search')],
        [sg.Listbox(
            key='-OUTPUT-', values=[],
            select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, bind_return_key=True, enable_events=True, visible=False,
            size=(30, 20))]]

    return sg.Window('Friends', layout3, finalize=True, resizable=True, icon='img/steamlogo.ico', modal=True)


def friend_window():

    layout4 = [[sg.Text('niks')]]

    return sg.Window('Friend Games', layout4, finalize=True, resizable=True, icon='img/steamlogo.ico', modal=True)


'''def sorting_data(data):
    i = 0
    dic = {}
    while i < len(data):
        # Voegt de naam en de app id toe aan een dictionary
        dic[data[i]['name']] = data[i]['appid']
        i += 1

    return dic'''


def search_name(name, dic):
    return dic[name]


window1, window2, window3, window4 = dashboard(), None, None, None


while True:
    window, event, values = sg.read_all_windows()

    if event == sg.WIN_CLOSED or event == 'Exit::exitkey':

        window.close()

        if window == window2:
            window2 = None

        elif window == window3:
            window3 = None

        elif window == window4:
            window4 = None

        elif window == window1:
            break

    elif event == 'Help::help':
        sg.Popup('Contact me: Luuk.Munneke@student.hu.nl', title='Help')

    elif event == 'Games::Gameskey' and not window2:  # Opent Game window
        window2 = Game_window()

    elif event == 'listbox_g':  # Window 2
        name = values[event]
        keydic = name[0]

    elif event == 'Friends::friendskey' and not window3:  # Opent Friend List window
        window3 = friend_list_window()

    elif event == 'Search':

        if not values['-INPUT-']:
            window['-OUTPUT-'].update(f"Results: \nName not found")  # Als de naam niet gevonden is
        else:
            steamid = get_steamid(values['-INPUT-'])  # Krijgt de steamid van de naam die is ingevoerd
            vriendlijst, name_steamid = get_friends(steamid)
            window['-OUTPUT-'].update(vriendlijst, visible=True)  # Update de listbox van vrienden

    elif event == '-OUTPUT-':  # Als er op een naam word geklikt
        window4 = friend_window()
        steamname = values['-OUTPUT-']
        keydicname = steamname[0]
        steamid1 = search_name(keydicname, name_steamid)
        print(steamid1)


window.close()
