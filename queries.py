
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
        origen=?    
"""
