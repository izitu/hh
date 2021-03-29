# это запускаем ВТОРЫМ - скачиваются вакансии
# из собраной информации - 100 крупнейших(лучших фирм) 100bighh.py
# информация скачивается в отдельный файл - связка по id ~250 файлов

import requests, openpyxl, json, os
from tqdm import *
def apitofile(api):
	try:
		data = (
			requests.get("https://api.hh.ru/vacancies?employer_id="+api+"&area=1").json())
		try:
			print(data['items'][0])
			with open("100bighh/" + api + ".api", "w", encoding="utf-8") as fh:
				fh.write(
					json.dumps(data,
							   ensure_ascii=False))  # преобразовываем словарь data в unicode-строку и записываем в файл
		except:
			pass
		#s_to_file = open(api+'.api', "w", encoding="utf-8")
		#s_to_file.write(str(todos))
		#s_to_file.close()
	except:
		pass

# читаем excel-файл
wb = openpyxl.load_workbook("100bighh/firms.xlsx")

# печатаем список листов
sheets = wb.sheetnames
for sheet in sheets:
	print(sheet)

# получаем активный лист
sheet = wb.active
rows = sheet.max_row
print(rows)

for i in tqdm(range(2, rows + 1)):
	cell = sheet.cell(row=i, column=1)
	firm_no = str(cell.value)
	cell = sheet.cell(row=i, column=2)
	firm_name = str(cell.value)
	cell = sheet.cell(row=i, column=3)
	firm_id = str(cell.value)
	print(firm_no, firm_name, firm_id)
	apitofile(firm_id)


