from bs4 import BeautifulSoup
import requests
import time
import json
import os


def enter_name():
    path = input('Имя html-файла: ')
    if path[-5:] != '.html':
        path += '.html'
    while not os.path.isfile(path):
        path = input('Такого файла нет. Введите имя html-файла: ')
        if path[-5:] != '.html':
            path += '.html'
    return path


file = open(enter_name(), 'r', encoding='utf-8')
html = file.read()
file.close()

soup = BeautifulSoup(html, features="html.parser")
table_len = len(soup.find('table', {'class': 'g_tbl'}).find_all('tr')) - 1
table = soup.find('table', {'class': 'g_tbl'}).find_all('tr')

god_list, i = [], 0
while i < table_len:
    god_list.append(table[i+1].find_next('a').text)
    i += 1

data = {}
for god in god_list:
    response = requests.get('https://godville.net/gods/api/'+god)
    data[god] = json.loads(response.text)
    print(f'Записываю номер {god_list.index(god)+1}, это {god}')
    time.sleep(5)

today = time.strftime("%d-%b-%Y", time.gmtime())
with open('new-'+today+'.json', 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, ensure_ascii=False)
