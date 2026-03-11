from . import requests_api as api
import pandas as pd

json_file = api.data_profesores
new_csv = pd.DataFrame(json_file)
new_csv.to_csv("profesores_pandas.csv", index=False)