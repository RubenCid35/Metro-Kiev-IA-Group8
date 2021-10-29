


GET_GRAPH_NODES: str = """
    SELECT id_station, nombre, linea, posx, posy FROM estaciones

"""


GET_GRAPH_EDGES: str = """
    SELECT destino, peso FROM conexiones WHERE origen=?
"""


GET_CONEXION: str = """
    SELECT destino, peso 
    FROM conexiones 
    WHERE 
        conn_id = (SELECT conn1 FROM estaciones WHERE origen=111) 
        OR conn_id = (SELECT conn1 FROM estaciones WHERE origen=111) 
        OR conn_id = (SELECT conn3 FROM estaciones WHERE origen=111)
"""