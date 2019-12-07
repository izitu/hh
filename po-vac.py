# https://api.hh.ru/vacancies?text=Data+scientist&area=1
# собрать, то что есть, и посмотреть глыбже
# основной интерес - скилсы и деньги

import json, requests

def apitofile(api):
	try:
		data = (
			requests.get(api).json())
		try:
			print(data['items'][0])
			with open('bigd.api', 'w', encoding='utf-8') as fh:
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
apitofile('https://api.hh.ru/vacancies?text=Big+data&area=1')
#apitofile('https://api.hh.ru/vacancies?text=Data+scientist&area=1')

try:
	with open('bigd.api', 'r', encoding='utf-8') as fh:
		data = json.load(fh)
		print(data)
except:
	print('нет вакансий')
	pass
print('Найдено ', len(data['items']))
for vac in range(0,len(data['items'])):
	if (data['items'][vac]['salary']) == None:
		fr = ''
		to = ''
	else:
		fr = data['items'][vac]['salary']['from']
		to = data['items'][vac]['salary']['to']
			#print(firm_name, data['items'][vac])#['name']['alternate_url']
	tt = data['items'][vac]['published_at'][:10].split('-')
	dt = tt[2]+'.'+tt[1]+'.'+tt[0]
	print( data['items'][vac]['name'], "|",data['items'][vac]['id'], "|",
				data['items'][vac]['snippet']['responsibility'], "|",data['items'][vac]['snippet']['requirement'], "|",
				data['items'][vac]['alternate_url'], "|", fr, to, "|", dt)
	fname = 'bigd/' + str(data['items'][vac]['id']) + '.api'
	uname = 'https://api.hh.ru/vacancies/' + data['items'][vac]['id']
	todos = (requests.get(uname).json())

	with open(fname, 'w', encoding='utf-8') as fh:
		fh.write(
			json.dumps(todos,
					   ensure_ascii=False))  # преобразовываем словарь data в unicode-строку и записываем в файл

exit(0)
#try:
with open('vacancies.api', 'r') as fh:
	data = json.load(fh)
	print(data)
#except:
#    print('нет вакансий')
#    pass
