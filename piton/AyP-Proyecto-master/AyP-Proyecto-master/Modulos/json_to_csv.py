from . import requests_api as api
import csv

json_file = api.data_profesores

fieldnames = json_file[0].keys()

def convert():
    with open("profesores.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for data in json_file:
            writer.writerow(data)
