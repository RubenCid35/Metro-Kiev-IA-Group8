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

LOCATIONS = [
(50,  150),  
(50,  210), 
(50,  260), 
(50,  320), 
(100, 320), 
(150, 320), 
(210, 320), 
(260, 320), 
(0, 150), 
(0, 150),
(0, 150),
(0, 150),
(0, 150),
(0, 150),
(0, 150),
(0, 150),
(0, 250), 
(0, 250),
(0, 250),
(0, 250),
(0, 250),
(0, 250),
(0, 250),
(0, 250),
(0, 350),
(0, 350),
(0, 350),
(0, 350),
(0, 350),
(0, 350),
(0, 350),
(0, 350),
(0, 450),
(0, 450),
(0, 450),
(0, 450),
(0, 450),
(0, 450),
(0, 450),
(0, 450),
(0, 550),
(0, 550),
(0, 550),
(0, 550),
(0, 550),
(0, 550),
(0, 550),
(0, 550),
(0, 650),
(0, 650),
(0, 650),
(0, 650),
(0, 650),
(0, 650),
]
for (_id, station_name, linea, x, y), (x1, y1) in zip(cursor1.execute(GET_GRAPH_NODES), LOCATIONS):
    print(_id, station_name, linea, x, y, x1, y1)


stations = [{'data': {'id': str(_id), 'name': station_name, 'linea': linea}, 'position': {'x': x1, 'y': y1}, 'locked': False, 'grabbable': True, "classes": None}
for (_id, station_name, linea, x, y), (x1, y1) in zip(cursor1.execute(GET_GRAPH_NODES), LOCATIONS)]
conexiones = [{'data': {'source': str(origen), 'target': str(destino), 'linea': linea}, "classes": None} for origen, destino, linea in cursor1.execute(GET_GRAPH_EDGES)]

station_listed = [{'label': f"{_id}-{station_name}", "value": _id} for _id, station_name, _, _, _ in cursor1.execute(GET_GRAPH_NODES)]

# ------- App Layout (HTML DESCRIPTION) -------------
metro_graph = cyto.Cytoscape(
            id="grafo-red-metro",
            layout={'name': 'preset'}, # , 
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
                },
                {
                    'selector': '.tomado',
                    'style': {
                        'background-color': 'yellow',
                        'line-color': 'yellow'
                    }
                }
                ]
        )

input_zone = html.Section([
            html.H1("Encuentra tu camino", style={"font-size": "40px"}),
            html.Label("Selecciona la estación origen:", style={"color": "black", "padding-left": "30px", "font-size": "25px"}),
            dcc.Dropdown(   id="origen-input",
                            options=station_listed,
                            className="input_zone",
                            multi=False,
                            style={"width": "60%", "padding-left": "30px", "padding-top": "10px"},
                            placeholder="Seleciona la Estación de Origen"),
            html.Div([], style={"width": "100%", 'height': "20px"}),
            html.Label("Selecciona la estación destino:", style={"color": "black", "padding-left": "30px", "font-size": "25px", 'padding-top': "20px"}),
            dcc.Dropdown(   id="destino-input",
                            options=station_listed,
                            className="input_zone",
                            multi=False,
                            style={"width": "60%", "padding-left": "30px", "padding-top": "10px"},
                            placeholder="Seleciona la Estación de destino"),
            html.Button("Get Path", id="btn-path")
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

@app.callback(Output('destino-input', 'value'),
              Input('btn-path', 'n-clicks'),
              State('grafo-red-metro', 'elements'))
def get_positions(btn1, grafo) -> None:
    with open('positions.json', 'w') as f: print(grafo, file=f)

# ------- App -------------------------

# Cuando acabemos debug debe de ser false
if '__main__' == __name__:
    app.run_server(debug=True)