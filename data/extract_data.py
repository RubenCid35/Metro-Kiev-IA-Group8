import sqlite3

# This file is used to generate and transfer all the data
with sqlite3.connect("estaciones.db") as conn:
    
    reader = conn.cursor()
    writer = conn.cursor()

    select_query = """SELECT id_station, linea FROM estaciones 
    """

    insert_query = """
            INSERT INTO conexiones(conn_id, origen,destino, linea, peso) VALUES (?, ?, ?, ?, ?)
    """
    estaciones: list[(int, int)] = [ data for data in reader.execute(select_query, "")]
    linea = 1
    for i in range(len(estaciones)):
        if estaciones[i][1] != linea:
            linea += 1
            continue

        if estaciones[i][0] % 100 != 28:
            conn_id = estaciones[i][0] * 1000 + estaciones[i+1][0]
            writer.execute(insert_query, (conn_id, estaciones[i][0], estaciones[i+1][0], estaciones[i][1], 0.0))
            print(f"[RIGTH CONN]{estaciones[i]}{estaciones[i+1]}")
             
        if estaciones[i][0] % 100 != 11:
            conn_id = estaciones[i][0] * 1000 + estaciones[i-1][0]
            writer.execute(insert_query, (conn_id, estaciones[i][0], estaciones[i-1][0], estaciones[i][1], 0.0))            
            print(f"[LEFT CONN]{estaciones[i]}{estaciones[i-1]}")