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
    [sg.Text(eerstespel, font=font)]

]  # Hoe de window eruit moet zien.


window = sg.Window('Steam', layout, finalize=True, resizable=True)  # Creert de window


while True:  # While loop om de gegevens uit de window te lezen en acties uit te voeren.
    event, values = window.read()

    if event == 'Exit::exitkey':
        break

    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break

window.close()
