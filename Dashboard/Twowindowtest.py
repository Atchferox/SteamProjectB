from sys import maxsize
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
    layout2 = [[sg.Text('Dit is window2')]
               ]
    return sg.Window('windoow2', layout2, finalize=True, resizable=True)


dashboard, window2 = dashboard(), None

while True:
    window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED or event == 'Exit::exitkey':
        window.close()

        if window == window2:
            window2 = None

        elif window == dashboard:
            break

    elif event == 'Games::Gameskey' and not window2:
        window2 = Gamewindow()

window.close()
