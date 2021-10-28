
# Imports

# Dash Related Imports
from types import GetSetDescriptorType
import dash 
import dash.html as html
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc # Libreria usada por los StyleSheet predefinidos
import dash_cytoscape as cyto
from dash.dependencies import Input, State, Output

# Algoritmo

# Data Loading
import sqlite3
from queries import GET_GRAPH_NODES

from random import randint
# ------- App Creation && Global Configuration ------------

app = dash.Dash("metro-kiev-grupo-1", external_stylesheets=[dbc.themes.GRID, dbc.themes.LUMEN])

# ------- Data Loading

database_conn = sqlite3.connect("./data/estaciones.db")
cursor1 = database_conn.cursor() 

stations = [{'data': {'id': str(_id), 'name': station_name, 'linea': linea}, 'position': {'x': randint(1, 500), 'y': randint(1, 500)}, 'locked': True, 'grabbable': False}
for _id, station_name, linea, x, y in cursor1.execute(GET_GRAPH_NODES)]

station_listed = [{'label': f"{_id}-{station_name}", "value": _id} for _id, station_name, _, _, _ in cursor1.execute(GET_GRAPH_NODES)]


# ------- App Layout (HTML DESCRIPTION) -------------

app.layout = html.Div()
app.layout = html.Div([
    html.Div([
        cyto.Cytoscape(
            id="grefo-red-metro",
            autolock= True,
            layout={'name': 'preset'},
            elements=stations,
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
                }
            ]
        )
    ], className="mainframe"),
    html.Div([
        html.Div([
            html.H3("HALLA EL CAMINO"),

        ]),
        html.Div(id="path-container")
    ], className="mainframe")    
])

# ------- App Callbacks (FOR MAKING THE APP INTERACTIVE) ------------


if '__main__' == __name__:
    app.run_server(debug=True)
    # Cuando acabemos debug debe de ser false