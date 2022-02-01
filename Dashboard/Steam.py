'''
Voor dit programma moeten er een paar dingen worden geinstalleerd. 
Ten eerste, PySimpleGUI, dit doe je met pip install PySimpleGUI.
Ten tweede, Matplotlib, dit doe je met pip install matplotlib
Ten derde, Paraminko, dit doe je met pip install paramiko


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
    '''Combineerd de canvas met de diagram die je wil weergeven'''
    # figure_canvas_agg is een soort adres van een figure
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()

    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

    # slaat het 'adres' van de diagram op om later aan te roepen
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
        # roept de diagram die reeds wordt getoond aan om die vervolgens te verwijderen
        figure_canvas_agg = figure_dic[key]
        figure_canvas_agg.get_tk_widget().destroy()  # verwijdert de diagram
        plt.clf()
        # plt.title('')
    except (KeyError, NameError):
        pass

    names = ['Positieve reviews', 'Negatieve reviews']
    colors = ['#60B6E7', '#E06363']

    fig = plt.figure(figsize=(3, 3), facecolor='#1C1E23')
    fig.add_subplot(111).bar(names, values, width=0.4,
                             align='center', color=colors)
    plt.ylim(0, 100)

    plt.title('Reviews', color='white')
    plt.tick_params(colors='white')

    return draw_figure(window[key].TKCanvas, fig, key)


def search_name(name, dic):
    return dic[name]


def dashboard():
    topgames, listofids = top100games()

    # Hier komen de menu opties in. ['menu'['alles wat in het menu komt']]
    menu_def = [
        ['Steam', ['Friends::friendskey', 'Help::help', 'About',
                   '---', 'Contact Steam', '---', 'Exit::exitkey']],
        ['Library', ['Games::Gameskey']],
        ['Status', ['Online::online', 'Offline::offline', 'AFK::afk']]
    ]

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
                   [sg.Input(size=(25, 20), key='-GSEARCH-'),
                    sg.Button('Search', key='dashboard_search')],

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
                   [sg.Frame(title='Pi', layout=connect_layout,
                             pad=12, font=font2)]
                   ]
    # Hier worden de statistieken getoont
    stats = [[sg.Text(text='', key='-STATS-', font=font2)]]

    # Matplotlib canvas
    figure_canvas = [[sg.Text(key='-TITEL-', font=font)],
                     [sg.Text(key='-GAMEINFO-', font=font2)],
                     [sg.Canvas(key='-Dashboard_Review_Canvas-')],
                     [sg.Frame(title='Stats', layout=stats, border_width=1,
                               key='-STATSFR-', visible=False, font=font2)]
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
            hostnamesaved = hostname
            usernamesaved = username
            passwordsaved = password
            connect_ssh(hostnamesaved, usernamesaved,
                        passwordsaved, 'helloworld().py')

    elif event == 'Online::online':
        if (hostname, username, password) == ('Hostadress', 'Username', 'Password'):
            sg.Popup('Vul eerst de gegevens voor de pi in', title='Error')

        else:
            # hostnamesaved, usernamesaved, passwordsaved, online
            pass

    elif event == 'Offline::offline':
        if (hostname, username, password) == ('Hostadress', 'Username', 'Password'):
            sg.Popup('Vul eerst de gegevens voor de pi in', title='Error')

        else:
            # hostnamesaved, usernamesaved, passwordsaved, offline
            pass

    elif event == 'AFK::afk':
        if (hostname, username, password) == ('Hostadress', 'Username', 'Password'):
            sg.Popup('Vul eerst de gegevens voor de pi in', title='Error')

        else:
            # hostnamesaved, usernamesaved, passwordsaved, afk
            pass

    elif event == 'dashboard_search':
        window['-GSEARCH-'].update('')

        '''binary search op ingevoerde gamenaam'''
        game_input = values['-GSEARCH-']
        find_game = binary_search(game_input)

        if find_game == '404NotFound':
            # Game naam niet gevonden
            try:
                figure_canvas_agg = figure_dic['-Dashboard_Review_Canvas-']

                # maakt canvas leeg
                figure_canvas_agg.get_tk_widget().destroy()
            except KeyError:
                pass

            # update stats met foutmelding
            window['-STATSFR-'].update(visible=True)
            window['-STATS-'].update(
                'Game niet gevonden, \nprobeer de volledige naam in te typen')
            window['-TITEL-'].update(visible=False)
            window['-GAMEINFO-'].update(visible=False)

        else:
            window['-ZOEK-'].update('Game gevonden!')

            appid = get_appid(find_game)
            # get statistics
            avg_speeltijd = get_average_playtime(appid)
            estimate_owners = get_estimate_owners(appid)
            review_percentage = get_review_values(find_game)
            prijs, genre = get_game_info(appid)

            # In de GUI zetten
            produce_bar_diagram(review_percentage,
                                '-Dashboard_Review_Canvas-', find_game)
            window['-TITEL-'].update(find_game, visible=True)
            window['-GAMEINFO-'].update(
                f'Prijs: {prijs}\nGenre: {genre}', visible=True)
            window['-STATSFR-'].update(visible=True)
            window['-STATS-'].update(
                f"De gemiddelde speeltijd is {avg_speeltijd} \nSchatting aantal gebruikers: {estimate_owners}")

    elif event == 'Search':     # Vrienden zoeken

        if not values['-INPUT-']:
            # Als de naam niet gevonden is
            window['-OUTPUT-'].update(f"Results: \nName not found")

        else:
            # Krijgt de steamid van de naam die is ingevoerd
            steamid = get_steamid(values['-INPUT-'])
            vriendlijst, name_steamid = get_friends(steamid)

            # Update de listbox van vrienden
            window['-OUTPUT-'].update(vriendlijst,
                                      visible=True, disabled=False)

    elif event == '-OUTPUT-':  # Als er op een naam word geklikt
        steamname = values['-OUTPUT-'][0]

        # Geeft steamid om de lijst van games te krijgen
        steamid1 = search_name(steamname, name_steamid)
        gameidlijst, gamenames, playintimes = get_games(steamid1)

        # Als iemand geen games heeft
        if gamenames == None:
            window['-LISTGAMES-'].update(values=['Geen Games'], visible=True)

        else:
            # Maakt 2 dictionaries om dingen in op te slaan die we later nodig hebben
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
                # Reviews in matplotlib
                review_percentage = get_review_values(selectedgame)
                produce_bar_diagram(review_percentage,
                                    '-Dashboard_Review_Canvas-', selectedgame)
                appid = get_appid(selectedgame)
                prijs, genre = get_game_info(appid)

                # Get statistics
                playtime = gamename_playtime[selectedgame]
                uurgespeeld = convert_min_to_hour(playtime)
                steamlvl = get_steamlvl(steamid1)
                status = get_status(steamid1)

                # Window met statistieken updaten
                window['-STATS-'].update(
                    f'Steam naam: {steamname} \nSteam level: {steamlvl} \nDeze user is {status} \nTotale speeltijd: {uurgespeeld}')
                window['-STATSFR-'].update(visible=True)
                window['-TITEL-'].update(selectedgame)
                window['-GAMEINFO-'].update(f'Prijs: {prijs}\nGenre: {genre}')

        except (KeyError, NameError):
            print('Je kan dit niet selecteren')


window.close()
