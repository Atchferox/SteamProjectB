import PySimpleGUI as sg
import json

sg.theme('darkgray10')
font = ("Montserrat Extra Light", 20)

with open('deelsteam.json', 'r') as f:
    data = json.load(f)
    eerstespel = data[0]["name"]

menu_def = [['Steam', ['Friends::friendskey', 'Help', 'About', '---', 'Contact Steam', '---', 'Exit::exitkey']],
            ['Library', ['Games']]
            ]

layout = [
    [sg.Menu(menu_def)],
    [sg.Text(eerstespel, justification='center', font=font)]
]


window = sg.Window('Steam', layout, resizable=True).maximize()
window.maximize()


while True:
    event, values = window.read()

    if event == 'Exit::exitkey':
        break

    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

window.close()
