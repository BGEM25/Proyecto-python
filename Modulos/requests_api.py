import requests
#import json
#import csv
#import pandas

profesores_url = ("https://raw.githubusercontent.com/xdxvlxlx/AyP-Proyecto/refs/heads/master/profesores.json")
materias_url = ("https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/materias2526-1.json")

#def descargar():
response_materias = requests.get(materias_url)
response_profesores = requests.get(profesores_url)

data_materias = response_materias.json()
data_profesores = response_profesores.json()

#print(json.dumps(data_profesores, indent=1))
#with open("profesores.csv", "w") as file:
#    file.write(json.dumps(data_profesores, indent=1))


#if response.status_code == 200:
#    data = response.json()
#    print("Datos JSON Adquiridos")
#    print(json.dumps(data, indent=1))
#    #print(data)
#else:
#    print(f"A ocurrido un error, codigo {response.status_code}")
