# собрать данные о компаниях в данной области
# сначала собираем инфу по фирмам
# потом смотрим все вакансии этих фирм и заносим в файлик
# https://hh.ru/employers_company/medicina_farmacevtika_apteki?vacanciesRequired=true
import requests
import bs4
import time
import json
import os
import pandas as pd


def del_all_file():
    mypath = "obl"  # Enter your path here
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))


def webtofile():
    # сохраняем в файл нашу страницу

    base_url = 'https://hh.ru/employers_company/medicina_farmacevtika_apteki?vacanciesRequired=true'
    headers = {'accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    session = requests.Session()
    s0 = session.get(base_url, headers=headers)
    b = bs4.BeautifulSoup(s0.text, "html.parser")

    # f_all_row = b.findall(tr)
    # режим экономии
    s_to_file = open("obl\index_0_raw.html", "w", encoding="utf-8")
    s_to_file.write(str(b))
    s_to_file.close()
    fnum = b.find_all('a', class_='bloko-button HH-Pager-Control')
    if b.find(text='дальше'):
        print('продолжаем')
    else:
        print('других страниц нет - выход')
        exit(1)
    # если нет -- значит список пуст
    print(fnum[-1].get('href'))
    # разобрали на части ссылку - достали количество страниц
    all_num = int(fnum[-1].get('href').split('page=')[-1].split('&')[0])
    print(all_num)

    for num_str in range(1, all_num + 1):
        time.sleep(5)
        get_url = f'https://hh.ru/employers_company/medicina_farmacevtika_apteki?page={num_str}&vacanciesRequired=true'
        print(get_url)

        session = requests.Session()
        s0 = session.get(get_url, headers=headers)
        b = bs4.BeautifulSoup(s0.text, "html.parser")
        s_to_file = open(f"obl\index_{num_str}_raw.html", "w", encoding="utf-8")
        s_to_file.write(str(b))
        s_to_file.close()


# сколько файлов в директории
def find_num():
    # удаляем файл с данными перед созданием нового
    all_url_firm = 'obl\data.json'
    if os.path.exists(all_url_firm):
        os.remove(all_url_firm)

    # теперь нужно узнать сколько файлов в директории, что бы перебрать их
    num_f = int(0)
    files = os.listdir(path="obl")
    print(files)
    for fi in files:
        if "_raw.html" in fi:
            f = fi.split('_')
            print(f[1])
            nu = int(f[1])
            if num_f < nu:
                num_f = nu
    print(num_f)
    return num_f

def wr_to_file():
    print('Найдено страниц: ', find_num())
    all_text = []

    # перебираем страницы в поисках ссылок на фирмы с вакансиями и записываем в файл
    for page in range(find_num() + 1):
        print(f'Обрабатывается страница {page}')
        open_raw = open(f"obl\index_{page}_raw.html", "r", encoding="utf-8")
        s1 = open_raw.read()
        b = bs4.BeautifulSoup(s1, "html.parser")
        open_raw.close()
        firm_url_on_page = b.find_all('div', class_='employers-company__item') # span - employers-company__description

        for firm in firm_url_on_page:
            it = firm.find('a')
            firm_vak = firm.find("span", class_="employers-company__vacancies-count").text
            firm_url = 'https://hh.ru' + it.get('href')
            firm_txt = it.text
            firm_id = it.get('href').split("/")[-1]
            print(firm_id, firm_txt, firm_url, firm_vak)
            all_text.append([firm_id, firm_txt, firm_url, firm_vak])

    # закинем знания в эксель
    alt_p = pd.DataFrame(all_text, columns=("id", "name", "url", "vak"))
    alt_p.to_excel("obl/al-firm.xls", index=False)
    with open('obl\data.json', 'w', encoding='utf-8') as outfile:
        str_ = json.dumps(all_text, ensure_ascii=False)
        outfile.write(str_)

# 1 сначала все удаляем в директории
# del_all_file()

# 2 потом скачиваем страницы со списком фирм с вакансиями
# webtofile()

# 3 записываем ссылки в файл
# wr_to_file()

with open('obl\data.json', encoding='utf-8') as data_file:
     data_loaded = json.load(data_file, strict=False)

print(data_loaded)
print(len(data_loaded))


exit(0)
json_file = {'name':["aparna", "pankaj", "sudhir", "Geeku"],'degree': ["MBA", "BCA", "M.Tech", "MBA"],'score':[90, 40, 80, 98]}
df = pandas.DataFrame(json_file).to_excel("excel.xlsx")