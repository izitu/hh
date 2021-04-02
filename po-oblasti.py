# собрать данные о компаниях в данной области
# сначала собираем инфу по фирмам
# потом смотрим все вакансии этих фирм и заносим в файлик
# https://hh.ru/employers_company/medicina_farmacevtika_apteki?vacanciesRequired=true

import bs4
import time
import pandas as pd
from vaktojsonfunc import *
from tqdm import *


def del_all_file():
    mypath = "obl"
    print(f"Удаляем все в директории {mypath}")
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))


def webtofile():
    # сохраняем в файл нашу страницу
    base_url = 'https://hh.ru/employers_company/medicina_farmacevtika_apteki?vacanciesRequired=true'
    print(f"Сохраняем все фирмы с вакансиями в мед.сфере \n{base_url}")
    headers = {'accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    session = requests.Session()
    s0 = session.get(base_url, headers=headers)
    b = bs4.BeautifulSoup(s0.text, "html.parser")

    # f_all_row = b.findall(tr)
    # режим экономии
    s_to_file = open("obl/index_0_raw.html", "w", encoding="utf-8")
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
        time.sleep(3)
        get_url = f'https://hh.ru/employers_company/medicina_farmacevtika_apteki?page={num_str}&vacanciesRequired=true'
        print(get_url)

        session = requests.Session()
        s0 = session.get(get_url, headers=headers)
        b = bs4.BeautifulSoup(s0.text, "html.parser")
        s_to_file = open(f"obl/index_{num_str}_raw.html", "w", encoding="utf-8")
        s_to_file.write(str(b))
        s_to_file.close()


# сколько файлов в директории
def find_num():
    # удаляем файл с данными перед созданием нового
    all_url_firm = 'obl/data.json'
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
        open_raw = open(f"obl/index_{page}_raw.html", "r", encoding="utf-8")
        s1 = open_raw.read()
        b = bs4.BeautifulSoup(s1, "html.parser")
        open_raw.close()
        firm_url_on_page = b.find_all('div', class_='employers-company__item')  # span - employers-company__description

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
    alt_p.to_excel("obl/al-firm.xlsx")
    with open('obl/firm-url-id.json', 'w', encoding='utf-8') as outfile:
        str_ = json.dumps(all_text, ensure_ascii=False)
        outfile.write(str_)


def save_vak_to_json():
    with open('obl/firm-url-id.json', encoding='utf-8') as data_file:
        data_loaded = json.load(data_file, strict=False)

    print(data_loaded)
    print(len(data_loaded))
    for firm_id, firm_name, firm_url, firm_num_vak in tqdm(data_loaded):
        print(firm_id, firm_name)
        api_to_file("obl", firm_id)


# проверяем стопслова
def stop_slo(name):
    if name == "Администратор":
        return True
    if "Руководитель" in name:
        return False
    if "IT-специалист" in name:
        return False
    data_loaded = pd.read_excel("stop.xls", dtype=str)
    # print(data_loaded)
    for index, row in data_loaded.iterrows():
        # print(row['KEY'])
        slo = str(row['KEY'])
        # flag = slo in name.lower()
        # print(slo, "|", name.lower(), "|", flag)
        if slo in name.lower():
            print(f"{slo} => {name}")
            return True
    return False


def sborka():
    with open('obl/firm-url-id.json', encoding='utf-8') as data_file:
        data_loaded = json.load(data_file, strict=False)

    all_vak = []

    for firm_id, firm_name, firm_url, firm_num_vak in tqdm(data_loaded):

        print("\t", firm_id, firm_name)
        try:
            with open("obl/" + firm_id + ".json", "r", encoding="utf-8") as fh:
                data = json.load(fh)
            # print(data)
            vaks = data['items']
        except:
            # print('нет вакансий')
            continue

        for it in vaks:
            # скипаем по названию вакансий
            if stop_slo(it["name"]):
                # "Есть  - скипаем"
                continue
            # скипаем по требованиям
            if (it['snippet']['requirement'] is not None) and (stop_slo(it['snippet']['requirement'])):
                continue
            # print(it["id"], it["name"])
            if it['salary'] is None:
                fr = ''
                to = ''
            else:
                fr = it['salary']['from']
                to = it['salary']['to']
                # нам не нужно до 75тыр
                if (to is not None) and (int(to) < 75000):
                    continue
                # и если от 70 и пусто
                if (fr is not None) and (to is None) and (int(fr) < 70000):
                    continue
            if it['address'] is None:
                vak_metro = ''
            else:
                if it['address']['metro'] is None:
                    vak_metro = ''
                else:
                    vak_metro = it['address']['metro']['station_name']
                    # print(it['address']['metro']['station_name'])

            tt = it['published_at'][:10].split('-')
            dt = tt[2] + '.' + tt[1] + '.' + tt[0]
            vak_name = it['name']
            vak_resp = it['snippet']['responsibility']
            vak_req = it['snippet']['requirement']
            vak_url = it['alternate_url']
            all_vak.append([firm_name, firm_url, vak_name, vak_resp, vak_req, vak_url, fr, to, dt, vak_metro])  #
            # print(firm_name, it['name'], "|", it['snippet']['responsibility'], "|", it['snippet']['requirement'],
            #      "|", it['alternate_url'], "|", fr, to, "|", dt)
        all_vak_p = pd.DataFrame(all_vak, columns=(
            "ФИРМА", "URL", "ВАКАНСИЯ", "ОПИСАНИЕ", "ТРЕБОВАНИЯ", "URL", "ОТ", "ДО", "Дата", "МЕТРО"))
        all_vak_p.to_excel("obl/al-vak.xlsx")

    # with open('stop-dict.json', encoding='utf-8') as data_file:
    #    stopw = json.load(data_file, strict=False)
    # for nu, slo in stopw.items():
    #    if slo in name.lower():
    #        # print(f"{slo} => {name}")
    #        return True
    # return False


# -----------pandas.read_json("obl/firm-url-id.json").to_excel("obl/allfirms.xlsx")
# -----------data_loaded = pandas.read_excel("obl/allfirms.xlsx")
# #### КОРОЧЕ РАБОТАТЬ С ЭКСЕЛЕМ ПРОЩЕ - НУ ВОТ ТАК
# ----------------------------------------------------------------------------
# 1 ПЕРЕГОНЯЕМ СЛОВАРЬ В ЭКСЕЛЬ
# иногда нужно отредактировать в экселе и перегнать обратно
# работать удобнее когда у тебя json
# with open('stop-dict.json', encoding='utf-8') as data_file:
#     stopw = json.load(data_file, strict=False)
# d = pd.read_json("stop-dict.json", index=['0'])#
# p = pd.DataFrame(stopw[1])
# p.to_excel("stop-dict.xls")
# 2 ПЕРЕГОНЯЕМ СЛОВАРЬ ИЗ ЭКСЕЛЯ В JSON
# data_loaded = pd.read_excel("stop-dict.xls", dtype={'text': 'unicode'})
# data_loaded[0].str.encode('utf-8')
# with open(f"stop-dict.json", "w", encoding="utf-8") as fh:
#    data_loaded[0].to_json("stop-dict.json", force_ascii=False, indent=4)
# exit(0)
# файл json получается в win кодировке - приходится его конвертить
# как сделать сразу -- не знаю :((
# ----------------------------------------------------------------------------

# 1 сначала все удаляем в директории
# del_all_file()

# 2 потом скачиваем страницы со списком фирм с вакансиями
# webtofile()

# 3 записываем ссылки в файл
# wr_to_file()

# 4 Скачиваем все вакансии у всех фирм в json файлы
# save_vak_to_json()

# 5 Сборка из json-ов в один эксельный файл
sborka()
