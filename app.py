
# Imports
# Dash Related Imports
import dash 
from dash import html
from dash import dcc
import dash_cytoscape as cyto
from dash.dependencies import Input, State, Output  # Para los callbacks

# Algoritmo

# Data Loading
import sqlite3
from queries import GET_GRAPH_NODES, GET_GRAPH_EDGES

from random import randint

# ------- App Creation && Global Configuration ------------

app = dash.Dash("metro-kiev-grupo-1", assets_folder='assets')

# ------- Data Loading

database_conn = sqlite3.connect("./data/estaciones.db")
cursor1 = database_conn.cursor() 

stations = [{'data': {'id': str(_id), 'name': station_name, 'linea': linea}, 'position': {'x': randint(1, 500), 'y': randint(1, 500)}, 'locked': False, 'grabbable': True}

for _id, station_name, linea, x, y in cursor1.execute(GET_GRAPH_NODES)]
conexiones = [{'data': {'source': str(origen), 'target': str(destino), 'linea': linea}} for origen, destino, linea in cursor1.execute(GET_GRAPH_EDGES)]

station_listed = [{'label': f"{_id}-{station_name}", "value": _id} for _id, station_name, _, _, _ in cursor1.execute(GET_GRAPH_NODES)]

# ------- App Layout (HTML DESCRIPTION) -------------
metro_graph = cyto.Cytoscape(
            id="grefo-red-metro",
            layout={'name': 'grid'}, # , 
            style={'width': '45%', 'height': '700px','background-color': 'black', 'margin': '20px 20px 20px 20px', },
            elements=stations + conexiones,
            maxZoom=1,
            minZoom=0.75,
            stylesheet=[   
                {
                    'selector': 'node',
                    'style': {
                        'label': 'data(id)',
                        'color': 'white',
                        'font-size': '15px'
                    }
                },

                {
                    'selector': '[linea = 1]',
                    'style': {
                        'background-color': 'red',
                        'line-color': 'red'
                    }
                },
                
                {
                    'selector': '[linea = 2]',
                    'style': {
                        'background-color': 'blue',
                        'line-color': 'blue'
                    }
                },
                {
                    'selector': '[linea = 3]',
                    'style': {
                        'background-color': 'green',
                        'line-color': 'green'
                    }
                }
            ]
        )

input_zone = html.Section([
            html.H1("Encuentra tu camino", style={"color": "black", "padding-left": "30px"}),
            html.Label("Selecciona la estación origen:", style={"color": "black", "padding-left": "30px", "font-size": "20px"}),
            dcc.Dropdown(   id="origen-input",
                            options=station_listed,
                            className="input_zone",
                            multi=False,
                            style={"width": "75%", "padding-left": "30px", "padding-top": "10px"},
                            placeholder="Seleciona la Estación de Origen"),
            html.Div([], style={"width": "100%", 'height': "20px"}),
            html.Label("Selecciona la estación destino:", style={"color": "black", "padding-left": "30px", "font-size": "20px", 'padding-top': "20px"}),
            dcc.Dropdown(   id="destino-input",
                            options=station_listed,
                            className="input_zone",
                            multi=False,
                            style={"width": "75%", "padding-left": "30px", "padding-top": "10px"},
                            placeholder="Seleciona la Estación de destino"),
            
        ])

right_side = html.Div([
            html.Div([input_zone], style={'width': '100%', 'height': '50%', 'margin': '20px 20px 20px 20px', 'background-color': 'white', 'border-radius': '10%'}),
            html.Div(style={'width': '100%', 'height': '50%', 'margin': '20px 20px 20px 20px', 'background-color': 'white', 'border-radius': '10%'}, id="path-zone")
        ], style={'width': "50%", 'heigth': '50%'})

app.layout = html.Div([
    html.Div([html.H1("LINEA DE METRO DE KIEV: BUSCA TU CAMINO")], style={'text-align':"center", 'margin': '20px 20px 20px 20px'}),
    html.Div([metro_graph, right_side], style={'display': 'flex'})
])
"""
dbc.Row([
            html.H2("LOOKING THE WAY"),,

            html.Label("Estación de Partida(Origen): "),
            dcc.Dropdown(   id="origen-input",
                            options=station_listed,
                            className="input_zone",
                            multi=False,
                            placeholder="Seleciona la Estación de Partida"),
            
            html.Br,
            html.Label("Estación de Destino: "),
            dcc.Dropdown(   id="destino-input",
                            options=station_listed,
                            className="input_zone",
                            multi=False,
                            placeholder="Seleciona la Estación de Destino"),
        ]),
        dbc.Row([html.Div("Hola mundo", id="path-zone")])
        

"""




# ------- App Callbacks (FOR MAKING THE APP INTERACTIVE) ------------


# ------- App -------------------------

# Cuando acabemos debug debe de ser false
if '__main__' == __name__:
    app.run_server(debug=True)
    for data in stations:
        print(data['data']['id'], '-'.data['position']['x'], '-', data['position']['y'])
