import json

with open('deelsteam.json', 'r') as f:
    data = json.load(f)


i = 0
while i < len(data):
    print(data[i]["name"])
    i += 1
