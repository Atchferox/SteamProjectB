from msvcrt import kbhit
import PySimpleGUI as sg  # pip install PySimpleGUI
from ctypes import windll
from API.API import *

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Hierdoor is het op elk scherm high definition
windll.shcore.SetProcessDpiAwareness(1)

sg.theme('darkgray10')
font = ("Montserrat Extra Light", 18)  # test font
font2 = ("Montserrat Extra Light", 12)

figure_dic = {}
all_games_list = game_list()


def draw_figure(canvas, figure, key):
    ''''''
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    figure_dic[key] = figure_canvas_agg
    return figure_canvas_agg


def produce_bar_diagram(values, key, naam):
    '''Maakt staafdiagram'''

    try:  # Indien er al een diagram bestaat
        figure_canvas_agg = figure_dic[key]
        figure_canvas_agg.get_tk_widget().destroy()
        plt.clf()
        # plt.title('')
    except KeyError:
        pass
    except NameError:
        pass

    names = ['Positieve reviews', 'Negatieve reviews']
    colors = ['#60B6E7', '#E06363']

    fig = plt.figure(figsize=(3, 3), facecolor='#1C1E23')
    fig.add_subplot(111).bar(names, values, width=0.4, align='center', color=colors)
    plt.ylim(0, 100)
    plt.title(naam, color='white')
    plt.tick_params(colors='white')

    return draw_figure(window[key].TKCanvas, fig, key)


def dashboard():
    topgames, listofids = top100games()
    eerste = topgames[0]
    tweede = topgames[1]
    derde = topgames[2]
    vierde = topgames[3]
    vijfde = topgames[4]
    zes = topgames[5]
    zeven = topgames[6]
    acht = topgames[7]
    negen = topgames[8]
    tien = topgames[9]
    elf = topgames[10]
    twaalf = topgames[11]
    dertien = topgames[12]
    veertien = topgames[13]
    vijftien = topgames[14]

    menu_def = [['Steam', ['Friends::friendskey', 'Help::help', 'About', '---', 'Contact Steam', '---', 'Exit::exitkey']],
                ['Library', ['Games::Gameskey']]]  # Hier komen de menu opties in. ['menu'['alles wat in het menu komt']]

    pop_games = [[sg.Text('Populair nu', font=font)],
                 [sg.Text(text=eerste, pad=11, font=font2)],
                 [sg.Text(text=tweede, pad=11, font=font2)],
                 [sg.Text(text=derde, pad=11, font=font2)],
                 [sg.Text(text=vierde, pad=11, font=font2)],
                 [sg.Text(text=vijfde, pad=11, font=font2)],
                 [sg.Text(text=zes, pad=11, font=font2)],
                 [sg.Text(text=zeven, pad=11, font=font2)],
                 [sg.Text(text=acht, pad=11, font=font2)],
                 [sg.Text(text=negen, pad=11, font=font2)],
                 [sg.Text(text=tien, pad=11, font=font2)],
                 [sg.Text(text=elf, pad=11, font=font2)],
                 [sg.Text(text=twaalf, pad=11, font=font2)],
                 [sg.Text(text=dertien, pad=11, font=font2)],
                 [sg.Text(text=veertien, pad=11, font=font2)],
                 [sg.Text(text=vijftien, pad=11, font=font2)],

                 ]

    tweedecolom = [
        # Search box
        [sg.Text('Search Games', font=font)], [sg.Input(size=(25, 20), pad=(12, 12), key='-GSEARCH-')],
        [sg.Button('Search', key='dashboard_search')],
        # Search Results
        [sg.Text(text='', key='-STATS-', visible=True, font=font2)],
        [sg.Listbox(key='-OUTPUT-', values=[],
                    select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, bind_return_key=True, enable_events=True, visible=False,
                    size=(30, 20)),
         ]
    ]

    figure_canvas = [[sg.Canvas(key='-Dashboard_Review_Canvas-')]]

    vriendenlijst = [[sg.Listbox(
        key='-OUTPUT-', values=[],
        select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, bind_return_key=True, enable_events=True, visible=False,
        size=(30, 20))]]

    gamelisjtvriend = [[sg.Listbox(
        key='-LISTGAMES-', values=[],
        select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, bind_return_key=True, enable_events=True, visible=False,
        size=(30, 20))]]

    layout = [[sg.Menu(menu_def)],

              [sg.Frame(title='', layout=pop_games, expand_y=True, element_justification='left'),
               sg.VerticalSeparator(),
               sg.vtop(sg.Frame(title='', layout=tweedecolom)),
               sg.Frame(title='', layout=figure_canvas, border_width=0)]

              ]

    return sg.Window('Steam Home Page', layout, size=(1280, 720),
                     finalize=True, resizable=True, icon='img/steamlogo.ico')


def Game_window():

    layout2 = [
        [sg.Text('Jouw Games', font=font)],
        [sg.Text('Deze functie is nog in ontwikkeling')]]

    return sg.Window('Games', layout2, finalize=True, resizable=True, icon='img/steamlogo.ico')


def friend_list_window():
    frame = [[sg.Listbox(
        key='-OUTPUT-', values=[],
        select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, bind_return_key=True, enable_events=True, visible=False,
        size=(30, 20))]]

    frame2 = [[sg.Listbox(
        key='-LISTGAMES-', values=[],
        select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, bind_return_key=True, enable_events=True, visible=False,
        size=(30, 20))]]

    layout3 = [
        [sg.Text('Vriendenlijst', font=font)],
        [sg.Text('Vul hier je steamID in om je vriendelijst te krijgen')],
        [sg.Input(do_not_clear=False, key='-INPUT-'),
         sg.Button('Search')],
        [sg.Frame(title='', layout=frame, border_width=0), sg.Frame(title='', layout=frame2, border_width=0)]]

    return sg.Window('Friends', layout3, finalize=True, resizable=True, icon='img/steamlogo.ico', modal=True)


def friend_window():

    steamname = values['-OUTPUT-']
    keydicname = steamname[0]

    steamid1 = search_name(keydicname, name_steamid)  # Geeft steamid om de lijst van games te krijgen
    gameidlijst, gamenames = get_games(steamid1)

    if gamenames == None:  # Als iemand geen games heeft
        gamenames = ['Geen games']

    else:
        gamenames_id = dict(zip(gamenames, gameidlijst))

    layout4 = [[sg.Listbox(values=gamenames, key='-GAMES-', size=(30, 10))],
               [sg.Text(key='-gekke-')]
               ]

    return sg.Window('Friend Games', layout4, finalize=True, resizable=True, icon='img/steamlogo.ico', modal=True)


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

    elif event == 'dashboard_search':
        '''binary search op ingevoerde gamenaam'''
        left = 0
        right = len(all_games_list) - 1
        game_input = values['-GSEARCH-']

        while left <= right:
            avg = int(left + (right - left) / 2)

            if all_games_list[avg].lower() == game_input.lower():
                window['-STATS-'].update(f'{all_games_list[avg]}')
                break

            elif all_games_list[avg] < game_input:
                left = left + 1
            elif all_games_list[avg] > game_input:
                right = right - 1
        else:
            window['-STATS-'].update('Game niet gevonden, \nprobeer de volledige naam in te typen')

    elif event == 'Friends::friendskey' and not window3:  # Opent Friend List window
        window3 = friend_list_window()

    elif event == 'Search':     # Vrienden zoeken

        if not values['-INPUT-']:
            window['-OUTPUT-'].update(f"Results: \nName not found")  # Als de naam niet gevonden is
        else:
            steamid = get_steamid(values['-INPUT-'])  # Krijgt de steamid van de naam die is ingevoerd
            vriendlijst, name_steamid = get_friends(steamid)
            window['-OUTPUT-'].update(vriendlijst, visible=True)  # Update de listbox van vrienden

    elif event == '-OUTPUT-':  # Als er op een naam word geklikt
        steamname = values['-OUTPUT-'][0]
        steamid1 = search_name(steamname, name_steamid)  # Geeft steamid om de lijst van games te krijgen
        gameidlijst, gamenames = get_games(steamid1)

        if gamenames == None:  # Als iemand geen games heeft
            gamenames = ['Geen games']
        else:
            gamenames_id = dict(zip(gamenames, gameidlijst))
        window['-LISTGAMES-'].update(values=gamenames, visible=True)

    elif event == '-LISTGAMES-':
        selectedgame = values['-LISTGAMES-'][0]
        try:
            appid = gamenames_id[selectedgame]
        except KeyError:
            print('Je kan dit niet selecteren')
        print(selectedgame, appid)


window.close()
