

# -----------------------------------------------
# Lista de Queries a usar para extraer los datos 
# de la base de datos. 
# Estas queries son de SQLite 
# -----------------------------------------------

GET_GRAPH_NODES: str = """
    SELECT id_station, nombre, linea, posx, posy FROM estaciones;
"""

GET_GRAPH_EDGES: str = """
    SELECT origen, destino, linea FROM conexiones;
"""


GET_CONEXION: str = """
    SELECT destino, peso, linea 
    FROM conexiones 
    WHERE 
        origen == ? AND
        destino != ?
"""