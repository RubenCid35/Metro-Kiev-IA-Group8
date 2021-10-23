
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


# ------- App Callbacks (FOR MAKING THE APP INTERACTIVE) ------------

@app.callback()
def crear_path() -> html.Div():
    pass


if '__main__' == __name__:
    app.run_server(debug=True)
    # Cuando acabemos debug debe de ser false