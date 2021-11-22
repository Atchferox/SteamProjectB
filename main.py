import json

f = open('deelsteam.json')

data = json.load(f)

i = 0
while i < len(data):
    print(data[i]["name"])
    i += 1
