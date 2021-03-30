import requests
import json

from numpy import random
from time import sleep


# записываем вакансии фирмы в файл
def api_to_file(save_dir, api):
    try:
        data = (
            requests.get("https://api.hh.ru/vacancies?employer_id=" + api + "&area=1").json())
        sleep_time = random.uniform(2, 5)
        print("sleeping for:", sleep_time, "seconds")
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


# проверяем словарь - если есть в словаре стоп слово - вакансию не печатаем dict
def stop_dict(name):
    with open('stop-dict.json', encoding='utf-8') as data_file:
        stopw = json.load(data_file, strict=False)
    for w in stopw:
        if name.count(w) != 0:
            return False
    return True
