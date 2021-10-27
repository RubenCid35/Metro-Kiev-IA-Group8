import sqlite3
import csv

# This file is used to generate and transfer all the data
with sqlite3.connect("estaciones.db") as conn, open("estaciones.csv") as f:
    
    # Para leer los datos del csv
    csvtool = csv.reader(f, delimiter=";")

    # Permite ejecutar queries 
    cursor = conn.cursor()

    query = """SELECT nombre FROM estaciones WHERE linea=?"""

    for data in cursor.execute(query, "3"):
        print(data)