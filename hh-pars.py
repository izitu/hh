# 100 лучших работодателей России
# https://hh.ru/article/303400

#import os, pandas
import requests, json
#from tqdm import *
#import pandas as pd
import csv
from bs4 import BeautifulSoup

# проверяем словарь - если есть в словаре стоп слово - вакансию не печатаем
def dict(name):
    stopw = ['АЗС','охр','Переводчик','Лаборант','питания', 'Химки','Электромонтер','1С','Механик','Электромонтажник','Водитель','ТРИЗ','логистике','технолог','продаж',
             'Эксплуатации','Оператор','HRBP','документообороту','простоя','Консультант','планово-экономического','сметной','Слесарь','делопроизводству']
    for w in stopw:
        if name.count(w)!=0:
            return False
    return True
# убираем скобки из названия вакансии
def skob(name):
    remw = ['«', '»','"']
    if name.count(remw[2]) != 0:
        name = name.replace(remw[2], '')
    if name.count(remw[0]) != 0:
        name = name.replace(remw[0], '')
        name = name.replace(remw[1], '')
    return name


#s0 = requests.get('https://hh.ru/search/vacancy?employer_id=102401&L_is_autosearch=false&area=1&clusters=true&enable_snippets=true')
#bs = BeautifulSoup(s0.text, "html.parser")



firm = ['Газпром', '10240']

hh_vak = requests.get('https://api.hh.ru/vacancies?employer_id=39305&area=1')#.json()
vac = json.loads(hh_vak.text)
#print(vac)
print("found",vac["found"])
print("pages",vac["pages"])


file = open('hh_jobs.csv','w')
a_pen = csv.writer(file, dialect='excel')
a_pen.writerow(('N', 'Название', 'Ценник', 'Чего делать', 'Чего хотят','URL'))
no = 0
for i in range(0, vac["pages"]):
    todos = (requests.get("https://api.hh.ru/vacancies?employer_id=39305&area=1", params={'page': i, 'per_page':20}).json())
    for i in range(0,20):
        try:
            if dict(todos['items'][i]['name']) :
                no = no + 1
                if (todos['items'][i]['salary']) == None:
                    print(no, todos['items'][i]['name'],"|",
                          todos['items'][i]['snippet']['responsibility'],"|",
                          todos['items'][i]['alternate_url'])
                    a_pen.writerow((no, todos['items'][i]['name'],todos['items'][i]['salary'],
                          todos['items'][i]['snippet']['responsibility'], todos['items'][i]['snippet']['requirement'], todos['items'][i]['alternate_url']))
                else:
                    print(no, todos['items'][i]['name'], "|",
                          todos['items'][i]['snippet']['responsibility'], "|",
                          todos['items'][i]['alternate_url'])
                    a_pen.writerow((no, todos['items'][i]['name'], todos['items'][i]['salary']['from'], todos['items'][i]['salary']['to'],
                          todos['items'][i]['snippet']['responsibility'],
                          todos['items'][i]['snippet']['requirement'], todos['items'][i]['alternate_url']))
        except:
            pass


file.close()
exit(0)
print("-----")
#print(todos["items"][0]["pages"])
print(todos["items"][7]["area"]["id"],todos["items"][7]["area"]["name"])
#print(["items"][0]["area"]["name"])
print("found",todos["found"])
print("pages",todos["pages"])
for i in tqdm(range(0, todos["pages"])):
    vac.append(requests.get("https://api.hh.ru/vacancies?employer_id=39305&area=1", params={'page': i, 'per_page':20}).json()['items'])


print(vac[id])
df = pd.DataFrame(vac)
print(df)

my_file_xml = open("vac-xml.txt", "w")
my_file_tab = open("vac-tab.txt", "w")
my_file_xml.write(str(vac))
my_file_tab.write(str(df))
my_file_xml.close()
my_file_tab.close()


# Увеличение выполненных задач каждым пользователем.
#for vaks in todos:
#    for vak in vaks:
#        print(vak['name'])
#print(vak[0])
exit(0)
#    if vak["name"]:
#        try:
#            print(todo["name"])
#            # Увеличение количества существующих пользователей.
#            #todos_by_user[todo["userId"]] += 1
#        except KeyError:
#            # Новый пользователь, ставим кол-во 1.
#            todos_by_user[todo["userId"]] = 1


response = requests.get("https://jsonplaceholder.typicode.com/todos")
todos = json.loads(response.text)
print (todos)
# Соотношение userId с числом выполненных пользователем задач.
todos_by_user = {}

# Увеличение выполненных задач каждым пользователем.
for todo in todos:
    if todo["completed"]:
        try:
            # Увеличение количества существующих пользователей.
            todos_by_user[todo["userId"]] += 1
        except KeyError:
            # Новый пользователь, ставим кол-во 1.
            todos_by_user[todo["userId"]] = 1

# Создание отсортированного списка пар (userId, num_complete).
top_users = sorted(todos_by_user.items(),
                   key=lambda x: x[1], reverse=True)

#Получение максимального количества выполненных задач.
max_complete = top_users[0][1]
print(max_complete)
# Создание списка всех пользователей, которые выполнили
# максимальное количество задач.
users = []
for user, num_complete in top_users:
    if num_complete < max_complete:
        break
    users.append(str(user))

max_users = " and ".join(users)

print(max_users)

s = "s" if len(users) > 1 else ""
print(f"user{s} {max_users} completed {max_complete} TODOs")
# users 5 and 10 completed 12 TODOs