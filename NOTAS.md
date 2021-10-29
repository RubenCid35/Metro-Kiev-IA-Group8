# NOTAS.md

En este archivo, pueden anotar dudas o ideas para el desarrollo del proyecto. 



html.Div([
        html.Div([
            html.H3("Get your Way", style={"color": 'darkRed'}),
            html.Label("Origen: "), html.Br,
             dcc.Dropdown(
               id="input-origen",
               options = station_listed,
               value=111,   
              ),html.Br,
            html.Label("Destino: "), html.Br,
             dcc.Dropdown(
               id="input-destino",
               options = station_listed,
               value=328,   
              ),html.Br,
            html.Button(
               id="get-path-btn"
            )
        ]),
        html.Div(
            id="path-container"
        )
    ]),