file_name = 'mas.txt'
with open(file_name, "r", encoding="utf-8") as fp:
    result = dict(map(str.split, fp))
print (result)
for key in result:
    print(key,result[key])
