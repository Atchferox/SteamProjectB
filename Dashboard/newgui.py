import PySimpleGUI as sg
import json

sg.theme('darkgray10')
font = ("Montserrat Extra Light", 20)

with open('deelsteam.json', 'r') as f:
    data = json.load(f)
    eerstespel = data[0]["name"]

menu_def = [['Steam', ['Friends::friendskey', 'Help', 'About', '---', 'Contact Steam', '---', 'Exit::exitkey']],
            ['Library', ['Games']]
            ]  # Hier komen de menu opties in. ['menu'['alles wat in het menu komt']]

layout = [
    [sg.Menu(menu_def)],
    [sg.Text(eerstespel, font=font)],
    [sg.Button('Window 2', key='Button')]

]  # Hoe de window eruit moet zien.

layout2 = [
    [sg.Text('window2 is open')]
]


window = sg.Window('Steam', layout, finalize=True, resizable=True)  # Creert de window
window2 = sg.Window('Games', layout2)

while True:  # While loop om de gegevens uit de window te lezen en acties uit te voeren.
    event, values = window.read()

    if event == 'Exit::exitkey' or event == sg.WINDOW_CLOSED or event == 'Quit':
        break

    

window.close()
