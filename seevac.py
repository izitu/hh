# смотрим вакансию конкретно
# 34790161
import json, re, requests

# у нас есть вакансия в дескрипшине которой есть все условия требовани и тд
# нам нужно найти - какие есть ключевые слова в описании (они гуляют и иногда называются по разному)
# найдем все теги со стронгом и двоеточием (пока с двоеточием)

fname = 'bigd/31756431.api'
#uname = 'https://api.hh.ru/vacancies/34790161'
#todos = (requests.get(uname).json())
#with open(fname, 'w') as f:
#    json.dump(todos, f)
p = re.compile(r'<.*?>')
with open(fname, 'r' , encoding='utf-8') as f:
	data = json.load(f)
print(data)
print(data['description'])
print(data['employer']['name'])
	#alldescr = p.sub('', data['description']) # убираем все теги
alldescr = data['description']

#if (alldescr.find('Условия:'))>0:
a = alldescr.split(':')
print(len(a))
wkey = [] # найденые ключевики запихиваем в лист
for i in range(0,len(a)):
	if i > 0: # ищем ключевики в предыдущем куске
		#print('---',a[i-1].split('<strong>')[-1])
		key = p.sub('',a[i-1].split('>')[-1])
		print('key - ',key.find('офис'))
		if (len(key)<40)and(key.find('офис')<0):
			wkey.append(key)
			print('---',p.sub('',a[i-1].split('>')[-1]))
	#print(f'Часть {i}')
	#print(a[i])
print(wkey, len(wkey))
# бьем строку по ключевикам
predpos = 0

for i, key in enumerate(wkey):
	fpos = alldescr.find(key)
	print(i, len(key), predpos, fpos, key, fpos-predpos)
	predpos = fpos
predpos = 0
for i, key in enumerate(wkey):
	fpos = alldescr.find(key) # ищем позицию ключа
	print('Номер: ', i, 'Ключ.сл.: "', key, '" Первая позиция: ',predpos, 'Вторая позиция:', fpos, '=', fpos-predpos)
	#if i == len(wkey):
	#	print(p.sub('',alldescr[predpos:]))#,' длина:' , len(p.sub('', alldescr[fpos:]).strip()))
	#else:
	tblock = p.sub('', alldescr[predpos:fpos])
	print(tblock) #,' длина:', len(tblock.strip()), len(key.strip()), key)
	#if fpos-predpos > 40:
	predpos = fpos
	#print(alldescr)
	#print(alldescr.split(key+':'))
#print(p.sub('',alldescr[:960]))
#print(p.sub('',alldescr[960:2064]))
#print(p.sub('',alldescr))
exit(0)
def opvac(id):
	#try:
	fullname = 'bigd/'+id+'.api'
	print(fullname)
	with open(fullname, 'r', encoding='utf-8') as fh:
		data = json.load(fh)
		print(data)


	#except:
	#	print('нет вакансий')
	#	pass


try:
	with open('bigd.api', 'r', encoding='utf-8') as fh:
		data = json.load(fh)
		#print(data)
except:
	print('нет вакансий')
	pass

print('Записей найдено:',len(data['items']))
p = re.compile(r'<.*?>')

for vac in range(0,len(data['items'])):
	#print(data['items'][vac])
	print('Название: '+data['items'][vac]['name'],'id: '+data['items'][vac]['id'],
		  'Компания: '+data['items'][vac]['employer']['name'],
		  'url: '+data['items'][vac]['employer']['alternate_url'])
	print('Требования (сокр): '+'Название: '+data['items'][vac]['snippet']['requirement'])

	try:
		print('Чего делать (сокр): ' + 'Название: ' + p.sub('', data['items'][vac]['snippet']['responsibility']))
	except:
		pass
	print('--->',data['items'][vac]['id'])
	opvac(data['items'][vac]['id'])