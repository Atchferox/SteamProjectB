'''
Voor dit programma moeten er een paar dingen worden geinstalleerd. 
Ten eerste, PySimpleGUI, dit doe je met pip install PySimpleGUI.
Ten tweede, Matplotlib, dit doe je met pip install matplotlib
Ten derde, Paraminko, dit doe je met pip install paraminko


Krijg je een fout melding als je dit programma probeert te openenen, ga dan naar de subdirectory Dashboard. 


Dit is een project van:
Luuk
Thomas
Ghassan
Maarten
Jasper
'''


import PySimpleGUI as sg
from ctypes import windll

from numpy import true_divide
from API.API import *
from API.ssh import *

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Hierdoor is het op elk scherm high definition
windll.shcore.SetProcessDpiAwareness(1)

sg.theme('darkgray10')
font = ("Montserrat Extra Light", 18)  # Titel font
font2 = ("Montserrat Extra Light", 12)  # Subtext font

figure_dic = {}
all_games_list = game_list()


def draw_figure(canvas, figure, key):
    ''''''
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    figure_dic[key] = figure_canvas_agg
    return figure_canvas_agg


def binary_search(game_input):
    left = 0
    right = len(all_games_list) - 1

    while left <= right:
        avg = int(left + (right - left) / 2)

        if all_games_list[avg].lower() == game_input.lower():
            return all_games_list[avg]

        elif all_games_list[avg] < game_input:
            left = left + 1
        elif all_games_list[avg] > game_input:
            right = right - 1
    else:
        return '404NotFound'


def get_review_values(naam):
    appid = get_appid(naam)
    review_values = get_steamspy(appid, 'reviews')
    review_percentage = [(review_values[0] / (review_values[0] + review_values[1])) * 100,
                         (review_values[1] / (review_values[0] + review_values[1])) * 100]
    return review_percentage


def produce_bar_diagram(values, key, naam):
    '''Maakt staafdiagram'''

    try:  # Indien er al een diagram bestaat
        figure_canvas_agg = figure_dic[key]
        figure_canvas_agg.get_tk_widget().destroy()
        plt.clf()
        # plt.title('')
    except (KeyError, NameError):
        pass

    names = ['Positieve reviews', 'Negatieve reviews']
    colors = ['#60B6E7', '#E06363']

    fig = plt.figure(figsize=(3, 3), facecolor='#1C1E23')
    fig.add_subplot(111).bar(names, values, width=0.4, align='center', color=colors)
    plt.ylim(0, 100)

    plt.title(naam, color='white')
    plt.tick_params(colors='white')

    return draw_figure(window[key].TKCanvas, fig, key)


def search_name(name, dic):
    return dic[name]


def dashboard():
    topgames, listofids = top100games()

    menu_def = [['Steam', ['Friends::friendskey', 'Help::help', 'About', '---', 'Contact Steam', '---', 'Exit::exitkey']],
                ['Library', ['Games::Gameskey']],
                ['Status', ['Online::online', 'Offline::offline', 'AFK::afk']]
                ]  # Hier komen de menu opties in. ['menu'['alles wat in het menu komt']]

    pop_games = [[sg.Text('Populaire Games', font=font)]]

    pop_games += [[sg.Text(text=f'{name}', pad=11, font=font2)]
                  for name in topgames]  # List comprehension to get all the names in text block

    # Raspberry pi connection inputs
    connect_layout = [[sg.Text('Connect to your Raspberry Pi', font=font2), sg.Button('Connect', key='-CONNECT-')],
                      [sg.Input('Hostadress', pad=5, key='-HOST-')],
                      [sg.Input('Username', pad=5, key='-UN-')],
                      [sg.Input('Password', pad=5, key='-PW-')]
                      ]

    # Binary search box, vriendenlijst en gamelijst
    tweedecolom = [[sg.Text('Search Games', font=font)],
                   [sg.Input(size=(25, 20), key='-GSEARCH-'), sg.Button('Search', key='dashboard_search')],

                   # Search Results
                   [sg.Text(text='', key='-ZOEK-', visible=True, font=font2)],

                   # Vrienden zoeken
                   [sg.HorizontalSeparator()],
                   [sg.Text('Vriendenlijst', font=font)],
                   [sg.Text('Vul hier je steamID in om je vriendelijst te krijgen')],
                   [sg.Input(do_not_clear=False, key='-INPUT-', size=(25, 30)),
                    sg.Button('Search')],

                   # Hier komt de lijst van vrienden
                   [sg.Listbox(key='-OUTPUT-', values=[],
                    select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, bind_return_key=True, enable_events=True, visible=True, disabled=True,
                    size=(30, 20)),

                    # Hier komt de lijst van games
                    sg.Listbox(
                       key='-LISTGAMES-', values=[],
                       select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, bind_return_key=True, enable_events=True, visible=False,
                       size=(30, 20))
                    ],
                   # Frame om alles in te zetten
                   [sg.Frame(title='Pi', layout=connect_layout, pad=12, font=font2)]
                   ]
    # Hier worden de statistieken getoont
    stats = [[sg.Text(text='', key='-STATS-', font=font2)]]

    # Matplotlib canvas
    figure_canvas = [[sg.Canvas(key='-Dashboard_Review_Canvas-')],
                     [sg.Frame(title='Stats', layout=stats, border_width=1, key='-STATSFR-', visible=False, font=font2)]
                     ]

    # Volledige layout van de main window
    layout = [[sg.Menu(menu_def)],

              [sg.Frame(title='', layout=pop_games, expand_y=True, element_justification='left'),
              sg.VerticalSeparator(),
              sg.vtop(sg.Frame(title='', layout=tweedecolom)),
              sg.vtop(sg.Frame(title='', layout=figure_canvas, border_width=0, pad=(20, 20)))]

              ]

    return sg.Window('Steam Home Page', layout, size=(1400, 760),
                     finalize=True, resizable=True, icon='img/steamlogo.ico')


window = dashboard()


# While loop waarin alle events die er gebeuren kunnen uitgelezen worden
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit::exitkey':
        break

    elif event == 'Help::help':
        sg.Popup('Contact me: Luuk.Munneke@student.hu.nl', title='Help')

    elif event == 'Games::Gameskey':
        sg.Popup('Niet actief', title='Error')

    elif event == 'Friends::friendskey':
        sg.Popup('Niet actief', title='Error')

    elif event == '-CONNECT-':
        hostname = values['-HOST-']
        username = values['-UN-']
        password = values['-PW-']
        if (hostname, username, password) == ('Hostadress', 'Username', 'Password'):
            sg.Popup('Vul eerst de gegevens voor de pi in', title='Error')
        else:
            # run file
            pass

    elif event == 'Online::online':
        hostname = values['-HOST-']
        username = values['-UN-']
        password = values['-PW-']
        if (hostname, username, password) == ('Hostadress', 'Username', 'Password'):
            sg.Popup('Vul eerst de gegevens voor de pi in', title='Error')
        else:
            # Run file
            pass

    elif event == 'Offline::offline':
        hostname = values['-HOST-']
        username = values['-UN-']
        password = values['-PW-']
        if (hostname, username, password) == ('Hostadress', 'Username', 'Password'):
            sg.Popup('Vul eerst de gegevens voor de pi in', title='Error')
        else:
            # Run file
            pass

    elif event == 'AFK::afk':
        hostname = values['-HOST-']
        username = values['-UN-']
        password = values['-PW-']
        if (hostname, username, password) == ('Hostadress', 'Username', 'Password'):
            sg.Popup('Vul eerst de gegevens voor de pi in', title='Error')
        else:
            # Run file
            pass

    elif event == 'dashboard_search':
        window['-ZOEK-'].update('')
        '''binary search op ingevoerde gamenaam'''
        game_input = values['-GSEARCH-']
        find_game = binary_search(game_input)
        if find_game == '404NotFound':
            figure_canvas_agg = figure_dic['-Dashboard_Review_Canvas-']
            figure_canvas_agg.get_tk_widget().destroy()
            window['-STATSFR-'].update(visible=True)
            window['-STATS-'].update('Game niet gevonden, \nprobeer de volledige naam in te typen')

        else:
            window['-ZOEK-'].update('Game gevonden!')
            appid = get_appid(find_game)
            avg_speeltijd = get_average_playtime(appid)
            estimate_owners = get_estimate_owners(appid)
            review_percentage = get_review_values(find_game)
            produce_bar_diagram(review_percentage, '-Dashboard_Review_Canvas-', find_game)
            window['-STATSFR-'].update(visible=True)
            window['-STATS-'].update(
                f"De gemiddelde speeltijd is {avg_speeltijd} \nSchatting aantal gebruikers: {estimate_owners}")

    elif event == 'Search':     # Vrienden zoeken

        if not values['-INPUT-']:
            window['-OUTPUT-'].update(f"Results: \nName not found")  # Als de naam niet gevonden is
        else:
            steamid = get_steamid(values['-INPUT-'])  # Krijgt de steamid van de naam die is ingevoerd
            vriendlijst, name_steamid = get_friends(steamid)
            window['-OUTPUT-'].update(vriendlijst, visible=True, disabled=False)  # Update de listbox van vrienden

    elif event == '-OUTPUT-':  # Als er op een naam word geklikt
        steamname = values['-OUTPUT-'][0]
        steamid1 = search_name(steamname, name_steamid)  # Geeft steamid om de lijst van games te krijgen
        gameidlijst, gamenames, playintimes = get_games(steamid1)

        if gamenames == None:  # Als iemand geen games heeft
            window['-LISTGAMES-'].update(values=['Geen Games'], visible=True)
        else:
            gamename_playtime = dict(zip(gamenames, playintimes))
            gamenames_id = dict(zip(gamenames, gameidlijst))
        window['-LISTGAMES-'].update(values=gamenames, visible=True)

    elif event == '-LISTGAMES-':
        selectedgame = values['-LISTGAMES-'][0]
        try:
            if selectedgame == 'Geen Games':
                figure_canvas_agg = figure_dic['-Dashboard_Review_Canvas-']
                figure_canvas_agg.get_tk_widget().destroy()
                window['-STATS-'].update('Deze user heeft geen spellen')
            else:
                review_percentage = get_review_values(selectedgame)
                produce_bar_diagram(review_percentage, '-Dashboard_Review_Canvas-', selectedgame)
                playtime = gamename_playtime[selectedgame]
                uurgespeeld = convert_min_to_hour(playtime)
                steamlvl = get_steamlvl(steamid1)
                window['-STATS-'].update(
                    f'Steam naam: {steamname} \nSteam level: {steamlvl} \nTotale speeltijd: {uurgespeeld}')
                window['-STATSFR-'].update(visible=True)

        except (KeyError, NameError):
            print('Je kan dit niet selecteren')


window.close()
