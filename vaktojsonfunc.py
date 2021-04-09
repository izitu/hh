import requests
import json
import os
from numpy import random
from time import sleep


# записываем вакансии фирмы в файл
def api_to_file(save_dir, api):
    if not os.path.exists(f"{save_dir}/{api}.json"):
        try:
            data = (
                requests.get("https://api.hh.ru/vacancies?employer_id=" + api + "&area=1").json())
            sleep_time = random.uniform(2, 4)
            print("sleeping for:", sleep_time, " seconds")
            sleep(sleep_time)

            try:
                print(data['items'][0])
                with open(f"{save_dir}/" + api + ".json", "w", encoding="utf-8") as fh:
                    # преобразовываем словарь data в unicode-строку и записываем в файл
                    fh.write(json.dumps(data, ensure_ascii=False))
            except:
                pass
        except:
            pass
    else:
        print(f"файл есть -- {save_dir}/{api}.json")


# проверяем словарь - если есть в словаре стоп слово - вакансию не печатаем dict
def stop_dict(name):
    with open('stop-dict.json', encoding='utf-8') as data_file:
        stopw = json.load(data_file, strict=False)
    for w in stopw:
        if name.count(w) != 0:
            return False
    return True


# перепишим функцию
# проверяем словарь - если есть в словаре стоп слово - вакансию не печатаем dict
def in_stop_dict(name):
    with open('stop-dict.json', encoding='utf-8') as data_file:
        stopw = json.load(data_file, strict=False)
    # print(name)
    name = str(name.lower())
    # print(name)
    for w in stopw:
        if name.count(w) != 0:
            # print(w)
            return True
    return False
