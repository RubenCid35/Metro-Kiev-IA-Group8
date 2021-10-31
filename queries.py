


GET_GRAPH_NODES: str = """
    SELECT id_station, nombre, linea, posx, posy FROM estaciones

"""

GET_GRAPH_EDGES: str = """
    SELECT origen, destino, linea FROM conexiones;
"""


GET_CONEXION: str = """
    SELECT destino, peso 
    FROM conexiones 
    WHERE 
        conn_id = (SELECT conn1 FROM estaciones WHERE origen=?) 
        OR conn_id = (SELECT conn2 FROM estaciones WHERE origen=?) 
        OR conn_id = (SELECT conn3 FROM estaciones WHERE origen=?)
"""

ADD_WEIGHT: str = """
    UPDATE TABLE conexiones WHERE 
"""
