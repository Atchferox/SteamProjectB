import PySimpleGUI as sg
import json

sg.theme('darkgray10')

with open('deelsteam.json', 'r') as f:
    data = json.load(f)
    eerstespel = data[0]["name"]


layout = [
    [sg.Text(eerstespel)],
    [sg.Button('Quit')]
]

window = sg.Window('Dashboard', layout)


while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
window.close()
