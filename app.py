
# Imports

# Dash Related Imports
import dash 
import dash.html as html
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc # Libreria usada por los StyleSheet predefinidos
from dash.dependencies import Input, State, Output

# Algoritmo

# Data Loading


# ------- App Creation && Global Configuration ------------

app = dash.Dash("metro-kiev-grupo-1")


# ------- App Layout (HTML DESCRIPTION) -------------

app.layout = html.Div()

# TODO Crear el Layout

# ------- App Callbacks (FOR MAKING THE APP INTERACTIVE) ------------

@app.callbackk()
def resaltar_origen(origen) -> str:
    """
    Debe resaltar el nodo origen en el grafo con un color para diferenciarlo
    """
    # TODO Implementar
    pass


@app.callback()
def crear_path_input(origin, destino1, grafo) -> html.Div(), str:
    """
    Toma el nodo de inicio del input y el nodo selecionado en el input o  el grafo:
    :param: origin. Nodo Origen. Obtenido del Input Origen de los nodos
    :param: destino1. Nodo Destino. Obtenido del Input Destino de los nodos.
    :param: **kwargs. Quitar si no se usa, solo era para que sepais que podeis añadir más datos
    """
    # TODO Implement
    # Nota: Debe de selecionar el nodo destino en le grafo
    pass


@app.callback()
def crear_path_grafo(origin, destino1) -> html.Div(), str:
    """
    Toma el nodo de inicio del input y el nodo selecionado en el input o  el grafo:
    :param: origin. Nodo Origen. Obtenido del Input Origen de los nodos
    :param: destino1. Nodo Destino. Es el nodo selecionado en el Grafo.
    :param: input_destino. Referencia al elemento del input Destino para cambiarlo
    """
    # TODO Implement
    # Nota: Debe de cambiar el nodo seleccionado en el Input de Destino.
    pass



if '__main__' == __name__:
    app.run_server(debug=True)
    # Cuando acabemos debug debe de ser false