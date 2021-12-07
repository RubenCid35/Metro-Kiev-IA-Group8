from typing import List
from queries import GET_CONEXION
import numpy as np 
import sqlite3

# Tabla con los valores 
HEURISTICA = np.loadtxt("./data/pesos.csv", delimiter=";")

def estacion_a_index(estacion) -> int:
    """
    Convierte un número de estación a una matriz de heuristica. 
    """
    linea = estacion // 100 - 1
    return linea * 18 + (estacion % 100) - 10


def heuristica(origen: int, destino: int) -> float:
    numeroNode = estacion_a_index(origen)
    numeroDestino = estacion_a_index(destino)
    return HEURISTICA[numeroNode, numeroDestino]

def get_path_from_list(cerrada, cursor):
    correct_list = [cerrada[-1][0]]
    for (estacion, _, _) in reversed(cerrada[:-1]):
        cursor.execute("SELECT destino from conexiones where origen==?", [correct_list[-1]])
        conexions = list(map(lambda x: x[0], cursor.fetchall()))
        if estacion in conexions:
            correct_list.append(estacion)

    return list(reversed(correct_list)), cerrada[-1][2]

def busqueda_camino(cursor, inicio, destino) -> List[str]:
    
    abierta = []
    cerrada = []
    
    # Nodo: Número de estacion, g(estacion), g(estacion) + h(estacion)
    abierta.append((inicio, 0, 0 + heuristica(inicio, destino)))

    while abierta != [] and  (cerrada == [] or cerrada[-1][0] != destino):
        # Ordenado de los valores de acuerdo a su peso más la heuristica
        abierta.sort(key = lambda x: x[2]) 

        # Evaluación del primer nodo
        cerrada.append(abierta.pop(0))

        # Añadir los nodos hijos
        for (dest,) in cursor.execute("SELECT destino from conexiones where origen==?", [cerrada[-1][0]]):
            
            # Precalculo de los valores
            gpeso = cerrada[-1][1] + heuristica(dest, cerrada[-1][0]) 
            total = gpeso + heuristica(dest, destino)
            
            # Busqueda dentro de la lista cerrada
            if any(map(lambda node: dest == node[0], cerrada)):
                continue
            # Busqueda dentro de la lista abierta
            elif idx := [i for i, estacion in enumerate(abierta) if estacion[0] == dest]:
                if abierta[idx[0]][2] < total:
                    abierta[idx[0]] = (dest, gpeso, total)
            
            # Añadido a la lista abierta
            else:
                abierta.append((dest, gpeso, total))
                                           
    return get_path_from_list(cerrada, cursor)



if __name__ == '__main__':
    # Para tests
    conn = sqlite3.connect("./data/estaciones.db")
    cursor = conn.cursor()
    print(busqueda_camino(cursor, 113, 218))