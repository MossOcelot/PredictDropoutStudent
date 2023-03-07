from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

@app.callback(
    Output("number-out", "children"),
    Input("dfalse", "value"),
)
def number_render(fval):
    return "dfalse: {}".format(fval)

def FromInputPage1():
    return html.Div([
            html.Div([
                html.P("รหัสนักศึกษา: ",style={'color':'white','font-size':'14px','margin':'0px'}),
                dcc.Input(id="dfalse", type="number", placeholder="Debounce False"),
                html.Div(id="number-out"),
            ], style={'display':'flex'})
        ])

def FromInputPage2():
    return html.Div([
        html.H3('Tab content 2')
    ])