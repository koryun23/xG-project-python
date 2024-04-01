import json
import pandas
from json_to_csv_converter import *

def extract_to_file():
    with open("Premier League/Premier League 2022-2023.json") as epl2023:
        data = json.load(epl2023)

    convert("Premier League/Premier League 2022-2023")
    data_frame = pandas.read_csv("Premier League/Premier League 2022-2023.csv")




