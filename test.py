import json
with open('prisoner_info.json','r',encoding='UTF-8') as f:
    all = json.load(f)
for i in all:
    print(i['имя'])