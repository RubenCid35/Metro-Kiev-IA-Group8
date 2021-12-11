# Imports
# Dash Related Imports
from os import truncate
import dash 
from dash import html
from dash import dcc
import dash_cytoscape as cyto
from dash.dependencies import Input, State, Output  # Para los callbacks

# Algoritmo
import busqueda as bq

# Data Loading
import sqlite3
from queries import GET_GRAPH_NODES, GET_GRAPH_EDGES

# ------- App Creation && Global Configuration ------------

app = dash.Dash(__name__, assets_folder='assets')
server = app.server
 

# ------- Data Loading

database_conn = sqlite3.connect("./data/estaciones.db", check_same_thread=False)

cursor = database_conn.cursor() 
cursor2 = database_conn.cursor()


stations = [{'data': {'id': str(_id), 'name': station_name, 'linea': linea}, 'position': {'x': x, 'y': y}, 'locked': True, 'grabbable': False, "classes": None}
for _id, station_name, linea, x, y in cursor.execute(GET_GRAPH_NODES)]
conexiones = [{'data': {'source': str(origen), 'target': str(destino), 'linea': linea}, "classes": None} for origen, destino, linea in cursor.execute(GET_GRAPH_EDGES)]

station_listed = [{'label': f"{_id}-{station_name}", "value": _id} for _id, station_name, _, _, _ in cursor.execute(GET_GRAPH_NODES)]

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
            html.H2("Encuentra tu camino", style={"font-size": "25px", "padding-left": "30px"}),
            html.Label("Selecciona la estación origen:", style={"color": "black", "padding-left": "30px", "font-size": "20px"}),
            dcc.Dropdown(   id="origen-input",
                            options=station_listed,
                            className="input_zone",
                            multi=False,
                            style={"width": "60%", "padding-left": "30px", "padding-top": "5px"},
                            placeholder="Seleciona la Estación de Origen"),
            html.Label("Selecciona la estación destino:", style={"color": "black", "padding-left": "30px", "font-size": "20px", "padding-top": "40px"}),
            dcc.Dropdown(   id="destino-input",
                            options=station_listed,
                            className="input_zone",
                            multi=False,
                            style={"width": "60%", "padding-left": "30px", "padding-top": "10px"},
                            placeholder="Seleciona la Estación de destino"),
            html.Button("Calcular Camino", id="btn-path", style={"margin-top": "20px", "width": "40%", "height": "40px", "margin-left": "30px", "font-size":"20px"})
        ])
# 
right_side = html.Div([
            html.Div([input_zone], style={'width': '100%', 'height': '50%', 'margin': '20px 20px 20px 20px', 'background-color': 'white'}),
            html.Div(style={'width': '100%','height': '60%', 'margin': '20px 20px 20px 20px', 'background-color': 'white'}, id="path-zone")
        ], style={'width': "50%", 'heigth': '50%'})

app.layout = html.Div([
    html.Div([html.H1("LINEA DE METRO DE KIEV: BUSCA TU CAMINO", style={"color": "white"})], style={'text-align':"center", 'margin': '20px 20px 20px 20px'}),
    html.Div([metro_graph, right_side], style={'display': 'flex'}),
    html.Div(id="hidden-div", style={"display":"none"})
])


# --------------- Pintar Camino ---------------------

path_styles = {
    '1': {"color": "red"},
    '2': {"color": "blue"},
    '3': {"color": "green"}
}



def pretify_path(lista_nodos):
    summaries = []
    text_stations = []
    lineas = []
    part = -1
    last_line = -1
    for nodo in lista_nodos:
        nombre = cursor2.execute("SELECT nombre FROM estaciones WHERE id_station=?", (nodo, )).fetchall()[0][0]
        if last_line != nodo[0]:
            summaries.append(f"Linea {nodo[0]}: Desde la estación: {nodo}-{nombre} a la estación: {nodo}-{nombre}")
            part = len(f"Linea {nodo[0]}: Desde la estación: {nodo}-{nombre} a la estación: ")
            text_stations.append([f"Se debe pasar por las siguientes estaciones", html.Br(), f"+ {nodo}-{nombre}"])
            lineas.append(nodo[0])
            last_line = lineas[-1]
        else:
            text_stations[-1] += [html.Br(), f"+ {nodo}-{nombre}"]
            summaries[-1] = summaries[-1][:part] + f"{nodo}-{nombre}"

    code = []
    for summ, text, linea in zip(summaries, text_stations, lineas):
        c = html.Details([
            html.Summary(summ),
            html.P(text)
        ], style=path_styles[linea], className="path-detail-text")
        code.append(c)

    return code


# ------- App Callbacks (FOR MAKING THE APP INTERACTIVE) ------------
@app.callback(
    Output("grafo-red-metro", 'elements'),
    Output('destino-input', 'value'),
    Output("path-zone", "children"),
    Output("origen-input", 'value'),
    Input("grafo-red-metro", 'tapNodeData'),
    Input("btn-path", "n_clicks"),    
    Input('destino-input', 'value'),
    State("grafo-red-metro", 'elements'),
    State("origen-input", 'value')
)
def cambiar_nodo_input(selected, _, dest, nodos, origen):
    """
    Si el nodo origen esta vacio, este se rellena sino se rellena el nodo destino con el nodo seleccionado en el grafo.
    Estos se deberian de pintar de amarillo.
    """
    triggered = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered == "grafo-red-metro":
        if origen is None:
            return nodos, dest, "", int(selected["id"])

        for v in nodos:
            if v["data"]["id"] == selected["id"]:
                v["classes"] = "tomado"
            else:
                v["classes"] = ""
        
        return nodos, int(selected["id"]), "", origen

    elif triggered == "destino-input":
        dest2 = str(dest)
        for v in nodos:
            if v["data"]["id"] == dest2:
                v["classes"] = "tomado"
            else:
                v["classes"] = ""
        
        return nodos, dest, "", origen
    else:
        if origen is None or dest is None:
            return nodos, dest, "", origen

        path = bq.busqueda_camino(cursor, origen, dest)
        nodos_itermedios = list(map(str, path[0]))
        for v in nodos:
            if v["data"]["id"] in nodos_itermedios:
                v["classes"] = "tomado"
            elif '-' in v["data"]["id"] and v["data"]["source"] in nodos_itermedios and v["data"]["target"] in nodos_itermedios:
                v["classes"] = "tomado"
            else:
                v["classes"] = ""

        return nodos, dest, pretify_path(nodos_itermedios), origen

# ------- App -------------------------

# Cuando acabemos debug debe de ser false
if __name__ == '__main__':
    app.run_server(debug=True)
