import pandas as pd

data_loaded = pd.read_excel("stop.xls", dtype=str)
# print(data_loaded)
for index, row in data_loaded.iterrows():
    print(row['KEY'])
    t = str(row['KEY'])
    print(t[1:])
exit(0)
file_name = 'mas.txt'
with open(file_name, "r", encoding="utf-8") as fp:
    result = dict(map(str.split, fp))
print (result)
for key in result:
    print(key,result[key])
