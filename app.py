
# Imports
# Dash Related Imports
import dash 
from dash import html
from dash import dcc
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc # Libreria usada por los StyleSheet predefinidos
import dash_cytoscape as cyto
from dash.dependencies import Input, State, Output

# Algoritmo

# Data Loading
import sqlite3
from queries import GET_GRAPH_NODES, GET_GRAPH_EDGES

from random import randint

# ------- App Creation && Global Configuration ------------

app = dash.Dash("metro-kiev-grupo-1", external_stylesheets=[dbc.themes.LUMEN])

# ------- Data Loading

def get_class(linea):
    if linea == 1:
        return 'red'
    elif linea == 2:
        return 'blue'
    elif linea == 3:
        return 'green'


database_conn = sqlite3.connect("./data/estaciones.db")
cursor1 = database_conn.cursor() 

stations = [{'data': {'id': str(_id), 'name': station_name, 'linea': linea}, 'position': {'x': randint(1, 500), 'y': randint(1, 500)}, 'locked': True, 'grabbable': False}

for _id, station_name, linea, x, y in cursor1.execute(GET_GRAPH_NODES)]
conexiones = [{'data': {'source': str(origen), 'target': str(destino)}, 'classes': get_class(linea)} for origen, destino, linea in cursor1.execute(GET_GRAPH_EDGES)]

station_listed = [{'label': f"{_id}-{station_name}", "value": _id} for _id, station_name, _, _, _ in cursor1.execute(GET_GRAPH_NODES)]


# ------- App Layout (HTML DESCRIPTION) -------------
metro_graph = cyto.Cytoscape(
            id="grefo-red-metro",
            autolock= True,
            layout={'name': 'preset'},
            elements=stations + conexiones,
            className="graph",
            stylesheet=[
                {
                    'selector': '[linea = 1]',
                    'style': {
                        'background-color': 'red'
                    }
                },
                
                {
                    'selector': '[linea = 2]',
                    'style': {
                        'background-color': 'blue',
                    }
                },
                {
                    'selector': '[linea = 3]',
                    'style': {
                        'background-color': 'green'
                    }
                },
                {
                    'selector': '.red',
                    'style': {
                        'line-color': 'red'
                    }
                },
                {
                    'selector': '.green',
                    'style': {
                        'line-color': 'green'
                    }
                },
                {
                    'selector': '.blue',
                    'style': {
                        'line-color': 'blue'
                    }
                }
            ]
        )

app.layout = html.Div([
    dbc.Col([
        html.Div(["hoal mudo", "da"])
    ]),
    dbc.Col([
        dbc.Row(html),
        dbc.Row(html.Div(id="path-zone"))
    ])
])





# ------- App Callbacks (FOR MAKING THE APP INTERACTIVE) ------------


# ------- App -------------------------

# Cuando acabemos debug debe de ser false
if '__main__' == __name__:
    app.run_server(debug=True)
