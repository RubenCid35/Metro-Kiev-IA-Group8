
from typing import List
from queries import GET_CONEXION

# TODO: Importar las librerias necesarias para el trabajo.

# NOTA: Se pueden crear más funciones auxiliares privadas para reducir redundancia en el código.

def h_tiempo(hora: int) -> float:
    pass

def heuristica(node: int, destino: int) -> float:
    pass


def get_path_from_list(cerrada: List[(int, float)]):
    return [data for (data,_) in cerrada]

def busqueda_camino(cursor, inicio, destino, hora):
    # TODO Implementar el algoritmo de A* para que devuelva el camino más corto
    # NOTA: lo de **kwargs es para añadir más parámetro por si queremos ajustarlo a 
    # la hora del día u otra cosa.
    
    abierta = []
    cerrada = []
    
    abierta.append((inicio, 0 + heuristica(inicio)))

    while cerrada != [] and  cerrada[-1][0] != destino:
        # Añadir los nodos hijos
        pass

    return get_path_from_list(cerrada)


def dijkstra_search(cursor, origen, destino) -> float:
    return 0