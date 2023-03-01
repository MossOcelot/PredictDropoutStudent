from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

app.layout = html.Div( 
    [
        dbc.Row(
            [
                html.Div(
                    dbc.Row([
                        html.I(className="bi bi-stack", style={'font-size': '28px', 'color': '#7465F1'}),
                        html.Div(style={'height': '2px', 'width':'52px','background':'white', 'margin-top': '20px', 'margin-bottom': '20px', 'margin-left': '6px'}),
                        html.I(className="bi bi-house-door-fill",style={'font-size': '28px', 'color': 'white'})
                    ], style={'text-align': 'center', 'margin-left': '0px'}),
                    style={'width': '76px','height': '100vh','background':'#292F45','padding-top':'20px'}
                ),
                dbc.Col([
                    html.Div([
                        html.Button("ติดต่อ",style={'width': '100px', 'height': '35px', 'color': 'white','border': '0px', 'background': '#7465F1', 'border-radius': '5px', 'margin-right': '36px'}),
                        html.Div(dbc.Col([
                            html.P("Phumin Sathipchan", style={'color':'white', 'margin': '0px', 'font-size': '12px'}),
                            html.P("Student", style= {'text-align': 'right','color':'white', 'margin': '0px', 'font-size': '12px'})
                        ],style={'display':'grid',"align-items": "center",'justify-content':'right', 'margin-right': '10px'}),
                        ),
                        html.Img(src="assets/profile.jpeg", style={'width': '50px','height': '50px','border-radius':'100%'}),
                        
                    ],style={'display': 'flex', 'align-items': 'center','justify-content':'right','padding-left': '13px', 'padding-right': '13px','margin-left': '23px', 'margin-top': '12px','background':'#292F45', 'width': '97%', 'height': '67px','border-radius': '5px' })
                ]),
            ]
        ),
    ],
    style={'background':'#171D31'}
)

if __name__ == "__main__":
    app.run_server(debug=True)
