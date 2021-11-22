
import sqlite3
import json


conn = sqlite3.connect("estaciones.db")

cursor = conn.cursor()
cursor2 = conn.cursor()


q = """
UPDATE estaciones SET posx={}, posy={} where station_id={};
"""

with open("tmp.sql", 'w', newline="\n") as file, open("positions.json",'r') as js:
    mx = 54
    data = json.load(js)
    print("[")
    for i, d in enumerate(data):
        if i == 54: break
        station  = d["data"]["id"]
        x = d["position"]["x"]
        y = d["position"]["y"]
        print(f"({x}, {y}),")
    print("]")