from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

# Input Prediction
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Input contact
@app.callback(
    Output("modal2", 'is_open'),
    [Input("open_contact", "n_clicks"), Input("open_contact2", "n_clicks")],
    [State("modal2", "is_open")]
)
def toggle_modal_contact(n1,n2,is_open):
    if n1 or n2:
        return not is_open
    return is_open

otherModels = []

for i in range(10):
    otherModels.append(
        html.Div([
            html.Div(html.P("Random Forest Classifier",style={'color':'white', 'margin': '0px', 'font-size': '14px'}),style={'width':'25%'}),
            html.Div([
                html.P("4 ฟีเจอร์",style={'color':'white', 'margin': '0px', 'font-size': '14px'}),
                html.P("(ADMIT_YEAR,  ADMIT_TERM, GPA_SCHOOL,....)",style={'color':'white', 'margin': '0px','margin-left':'3px', 'font-size': '8px'}),
            ],style={'display':'flex','align-items':'end','width':'47%'}),
            html.Div(html.P("94.3 %",style={'color':'white', 'margin': '0px', 'font-size': '14px'}),style={'width':'14%'}),
            html.Div(html.P("0.0810 sec",style={'color':'white', 'margin': '0px', 'font-size': '14px'}),style={'width':'14%'}),
        ],style={'display':'flex','padding-left':'20px','padding-right':'20px','align-items':'center','justify-content':'space-between','width':'804px','margin-top':'10px', 'height': '50px', 'border-bottom':'2px solid #353C56'})
    )

# -------------------- pie graph --------------------
values = [80,20]
# Create subplots: use 'domain' type for Pie subplot
fig = make_subplots(rows=1, cols=1, specs=[[{'type':'domain'}]])
fig.add_trace(go.Pie(values=values ),
              1, 1)

# Use `hole` to create a donut-like pie chart
fig.update_traces(hole=.7, hoverinfo="label+percent+name", textinfo='none')

fig.update_layout(
    height=700,margin=dict(t=0, b=0, l=0, r=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    # Add annotations in the center of the donut pies.
    showlegend=False,
    
    annotations=[dict(text='91.50%', x=0.5, y=0.6, font_size=16,  showarrow=False, font=dict(color="white")),
                 dict(text='ผ่าน', x=0.5, y=0.3, font_size=12,  showarrow=False, font=dict(color="white"))
                 ])

# -------------------- bar graph --------------------
# Define data for the bar chart
x = ['2559', '2560', '2561', '2562']
y = [30, 50, 20, 40]

# Create the bar chart
bar_chart = go.Figure(
    data=[go.Bar(x=x, y=y)],
    layout=go.Layout(title=''),
)

# Set the width and height to 100%
bar_chart.update_layout(
    autosize=True,
    height=83,
    width=160,
    margin=dict(t=0, b=0, l=0, r=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    
)

bar_chart.update_traces(marker=dict(color='#F8A22A',line=dict(width=1, color='#F8A22A')))
# Set color of x-axis tick labels
bar_chart.update_xaxes(tickfont=dict(color='white'))

# Set color of y-axis tick labels
bar_chart.update_yaxes(tickfont=dict(color='white'))

# -------------------- line graph --------------------
# Define data for the bar chart
x = ['2559', '2560', '2561', '2562']
y = [100, 50, 170, 200]

# Create the bar chart
line_chart = go.Figure(
    data=[go.Line(x=x, y=y)],
    layout=go.Layout(title=''),
)

# Set the width and height to 100%
line_chart.update_layout(
    autosize=True,
    height=83,
    width=160,
    margin=dict(t=0, b=0, l=0, r=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    
)

line_chart.update_traces(marker=dict(color='#12ABC3',line=dict(width=1, color='#12ABC3')))
# Set color of x-axis tick labels
line_chart.update_xaxes(tickfont=dict(color='white'))

# Set color of y-axis tick labels
line_chart.update_yaxes(tickfont=dict(color='white'))


app.layout = html.Div( 
    [
        dbc.Row(
            [
                html.Div(
                    dbc.Row([
                        html.I(className="bi bi-stack", style={'font-size': '28px', 'color': '#7465F1'}),
                        html.Div(style={'height': '2px', 'width':'52px','background':'white', 'margin-top': '20px', 'margin-bottom': '20px', 'margin-left': '6px'}),
                        html.I(className="bi bi-house-door-fill",style={'font-size': '28px', 'color': 'white'}),
                    ], style={'text-align': 'center', 'margin-left': '0px'}),
                    style={'width': '76px','height': '100','background':'#292F45','padding-top':'20px'}
                ),
                dbc.Col([
                    html.Div([
                        html.Button("ติดต่อ",id="open_contact",style={'width': '100px', 'height': '35px', 'color': 'white','border': '0px', 'background': '#7465F1', 'border-radius': '5px', 'margin-right': '36px'}),
                        # modal Contact
                        dbc.Modal([
                            dbc.ModalBody([
                                html.P("อาจารย์ที่ปรึกษา", style={'color':'white', 'margin': '0px', 'font-size': '16px'}),
                                html.Div([
                                    html.Img(src="assets/profile.jpeg", style={'width': '120px','height': '120px','border-radius':'100%'}),
                                    html.Div([
                                        html.P("นายภูมินทร์ สาทิพย์จันทร์", style={'color':'white', 'margin': '0px', 'font-size': '16px'}),
                                        html.P("เบอร์โทร: 099-999-9999", style={'color':'white', 'margin': '0px', 'font-size': '16px'}),
                                        html.P("email: phumin@gmail.com", style={'color':'white', 'margin': '0px', 'font-size': '16px'}),
                                        html.P("fax: 099-999-9998", style={'color':'white', 'margin': '0px', 'font-size': '16px'}),
                                    ], style={'margin-left':'10px'})
                                ], style={'display':'flex','padding':'20px','align-items':'center','margin-top':'30px','margin-bottom':'30px'})
                            ], style={
                                'background':'#292F45', 'border-radius': '5px'
                            }),
                            
                        ],
                        id="modal2",
                        is_open=False),
                        html.Div(dbc.Col([
                            html.P("Phumin Sathipchan", style={'color':'white', 'margin': '0px', 'font-size': '12px'}),
                            html.P("Student", style= {'text-align': 'right','color':'white', 'margin': '0px', 'font-size': '12px'})
                        ],style={'display':'grid',"align-items": "center",'justify-content':'right', 'margin-right': '10px'}),
                        ),
                        html.Img(src="assets/profile.jpeg", style={'width': '50px','height': '50px','border-radius':'100%'}),
                        
                    ],style={'display': 'flex', 'align-items': 'center','justify-content':'right','padding-left': '13px', 'padding-right': '13px','margin-left': '23px', 'margin-top': '12px','background':'#292F45', 'width': '97%', 'height': '67px','border-radius': '5px' }),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.P('โปรดกรอกข้อมูลของคุณ',style={'color':'white','font-size':'16px','margin':'0px'}),
                                    html.P('เพื่อคาดการณ์โอกาสการตกออก',style={'color':'white','font-size':'12px','margin':'0px', 'margin-top':'10px'})
                                ]),
                                html.Div([
                                    html.P('มีนักศึกษาร้อยละ 20 ที่มีโอกาสตกออก',style={'color':'white','font-size':'14px','margin':'0px'}),
                                    html.Button("คาดการณ์",id='open',style={'width': '100px', 'height': '35px', 'color': 'white','border': '0px', 'background': '#7465F1', 'border-radius': '5px', 'margin-right': '36px', 'margin-top': '8px'}),
                                    # modal input predict
                                    dbc.Modal([
                                        dbc.ModalHeader(dbc.ModalTitle("Header")),
                                        dbc.ModalBody("This is the content of the modal"),
                                        dbc.ModalFooter(
                                            dbc.Button(
                                                "Close", id="close", className="ms-auto", n_clicks=0
                                            )
                                        ),
                                    ],
                                    id="modal",
                                    is_open=False,),
                                ])
                            ],style={'display':'grid','align-content':'space-between','height': '143px',} ),
                            html.I(className="bi bi-question-circle-fill",style={'font-size': '108px', 'color': '#F8A22A'})

                        ],style={'display':'flex', 'align-items': 'end', 'justify-content': 'space-between','padding':'20px','background':'#292F45','width':'429px', 'height': '183px','border-radius': '5px'}),
                        html.Div([
                            html.Div([
                                html.P("สถิติ",style={'color':'white', 'font-size': '16px'}),
                                html.P("อัปเดตเมื่อวานนี้",style={'color':'white', 'font-size': '16px'})
                            ], style={'display': 'flex', 'justify-content': 'space-between'}),
                            html.Div([
                                html.Div([
                                    html.Div(html.I(className="bi-graph-up", style={'color': '#7064E7','font-size': '42px'}), style={'border-radius': '100%','padding-left':'20px','padding-right':'20px', 'padding-top':'10px', 'height': '80px', 'background': '#33375C'}),
                                    html.Div([
                                        html.P("700",style={'color':'white', 'font-size': '24px'}),
                                        html.P("จำนวนผู้เข้าร่วม",style={'color':'white', 'font-size': '12px'})
                                    ],style={'margin-left':'10px'})
                                ], style={'display': 'flex'}),
                                html.Div([
                                    html.Div(html.I(className="bi bi-shield-fill-check", style={'color': '#2AAB69','font-size': '42px'}), style={'border-radius': '100%','padding-left':'20px','padding-right':'20px', 'padding-top':'10px', 'height': '80px', 'background': '#2C434B'}),
                                    html.Div([
                                        html.P("500",style={'color':'white', 'font-size': '24px'}),
                                        html.P("จำนวนผู้ที่ผ่าน",style={'color':'white', 'font-size': '12px'})
                                    ],style={'margin-left':'10px'})
                                ], style={'display': 'flex'}),
                                html.Div([
                                    html.Div(html.I(className="bi bi-exclamation-triangle-fill", style={'color': '#E15354','font-size': '42px'}), style={'border-radius': '100%','padding-left':'20px','padding-right':'20px', 'padding-top':'10px', 'height': '80px', 'background': '#423747'}),
                                    html.Div([
                                        html.P("200",style={'color':'white', 'font-size': '24px'}),
                                        html.P("จำนวนผู้ที่ตกออก",style={'color':'white', 'font-size': '12px'})
                                    ],style={'margin-left':'10px'})
                                ], style={'display': 'flex'}),
                                html.Div([
                                    html.Div(html.I(className="bi bi-star-fill", style={'color': '#12ABC3','font-size': '42px'}), style={'border-radius': '100%','padding-left':'20px','padding-right':'20px', 'padding-top':'10px', 'height': '80px', 'background': '#2A445A'}),
                                    html.Div([
                                        html.P("700",style={'color':'white', 'font-size': '24px'}),
                                        html.P("จำนวนผู้เข้าร่วม",style={'color':'white', 'font-size': '12px'})
                                    ],style={'margin-left':'10px'})
                                ], style={'display': 'flex'})
                            ], style={'display': 'flex', 'justify-content': 'space-between','margin-top':'10px'}),
                        ],style={'padding':'20px','background':'#292F45','width':'875px', 'height': '183px','border-radius': '5px', 'margin-right': '15px'})
                    ],style={'display':'flex','justify-content':'space-between','margin-left': '23px','margin-top':'15px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.P("ความแม่นยำ",style={'color':'white', 'margin': '0px', 'font-size': '16px'}),
                                    html.P("40 %",style={'color':'white', 'margin': '0px', 'font-size': '24px'}),
                                    html.Div(
                                        dcc.Graph(id="example-graph-1",figure=bar_chart, style={'width':'147px', 'height':'73px','margin-top':'10px'})
                                    )
                                ],style={'width':'201px', 'height':'183px','background':'#292F45','border-radius': '5px','padding':'20px'}),
                                html.Div([
                                    html.P("จำนวนผลที่ตกออก",style={'color':'white', 'margin': '0px', 'font-size': '16px'}),
                                    html.P("200",style={'color':'white', 'margin': '0px', 'font-size': '24px'}),
                                    html.Div(
                                        dcc.Graph(id="example-graph-2",figure=line_chart, style={'width':'147px', 'height':'73px','margin-top':'10px'})
                                    )
                                ],style={'width':'201px', 'height':'183px','background':'#292F45','border-radius': '5px','padding':'20px'})
                            ], style={'display':'flex', 'justify-content':'space-between', 'width':'429px'}),
                            html.Div([
                                html.Div([
                                    html.P("สถานะ",style={'color':'white', 'margin': '0px', 'font-size': '16px'}),
                                    html.P("จำนวนนักศึกษาทั้งหมด",style={'color':'white', 'margin': '0px', 'font-size': '16px'}),
                                    html.Div([html.P("700",style={'color':'white', 'margin': '0px', 'font-size': '24px'}),html.P("คน",style={'color':'white', 'margin': '0px', 'font-size': '14px', 'margin-left': '5px', 'margin-bottom':'5px'})],style={'display':'flex', 'align-items':'end'}),
                                    html.P("มีจำนวนนักศึกษาที่จบ 80.5 % ใน 5 ปีที่ผ่านมา",style={'color':'white', 'margin': '0px', 'font-size': '11px'}),
                                ]),
                                html.Div([
                                    dcc.Graph(id="example-graph-3", figure=fig, style={'width':'110px', 'height':'110px'})
                                ]),
                            ],style={'display':'flex','justify-content':'space-between','background':'#292F45','width':'429px','height':'150px','margin-top':'15px','border-radius':'5px', 'padding':'20px'})
                        ]),
                        html.Div([
                            html.Div([
                                html.P("คำแนะนำเพิ่มเติม",style={'color':'white', 'margin': '0px', 'font-size': '16px'}),
                                html.Div([
                                    # recommend cards
                                    html.Div([
                                        html.I(className='bi bi-exclamation-diamond-fill', style={'font-size':'56px', 'color':'#F8A22A'}),
                                        html.P("ปีหน้าห้ามตก",style={'color':'white', 'margin': '0px', 'font-size': '16px','margin-left':'8px'})
                                    ],style={'display':'flex','align-items':'center','height':'80px', 'background':'#353C56','border-radius':'5px','padding':'20px','margin-right':'24px', 'margin-top':'15px'}),
                                    html.Div([
                                        html.I(className='bi bi-x-circle', style={'font-size':'56px', 'color':'#E15354'}),
                                        html.P("เทอมนี้ห้ามเกรดต่ำกว่า C ทุกตัว",style={'color':'white', 'margin': '0px', 'font-size': '16px','margin-left':'8px'})
                                    ],style={'display':'flex','align-items':'center','height':'80px', 'background':'#353C56','border-radius':'5px','padding':'20px','margin-right':'24px', 'margin-top':'15px'}),
                                    html.Div([
                                        html.I(className='bi bi-hand-thumbs-up-fill', style={'font-size':'56px', 'color':'#2AAB69'}),
                                        html.P("ตั้งใจเรียนต่อไป",style={'color':'white', 'margin': '0px', 'font-size': '16px','margin-left':'8px'})
                                    ],style={'display':'flex','align-items':'center','height':'80px', 'background':'#353C56','border-radius':'5px','padding':'20px','margin-right':'24px', 'margin-top':'15px'}),
                                    html.Div([
                                        html.I(className='bi bi-hand-thumbs-down-fill', style={'font-size':'56px', 'color':'#7465F1'}),
                                        html.P("ห้ามกินเหล้า",style={'color':'white', 'margin': '0px', 'font-size': '16px','margin-left':'8px'})
                                    ],style={'display':'flex','align-items':'center','height':'80px', 'background':'#353C56','border-radius':'5px','padding':'20px','margin-right':'24px', 'margin-top':'15px'}),
                                    html.Div([
                                        html.I(className='bi bi-hand-thumbs-up-fill', style={'font-size':'56px', 'color':'#2AAB69'}),
                                        html.P("โยนได้ปีหน้า",style={'color':'white', 'margin': '0px', 'font-size': '16px','margin-left':'8px'})
                                    ],style={'display':'flex','align-items':'center','height':'80px', 'background':'#353C56','border-radius':'5px','padding':'20px','margin-right':'24px', 'margin-top':'15px'}),
                                    html.Div([
                                        html.I(className='bi bi-hand-thumbs-down-fill', style={'font-size':'56px', 'color':'#7465F1'}),
                                        html.P("ห้ามเที่ยว",style={'color':'white', 'margin': '0px', 'font-size': '16px','margin-left':'8px'})
                                    ],style={'display':'flex','align-items':'center','height':'80px', 'background':'#353C56','border-radius':'5px','padding':'20px','margin-right':'24px', 'margin-top':'15px'})
                                ],style={'display':'grid', 'grid-template-columns':'281px 281px'})
                            ]),
                            html.Div(style={'width':'3px', 'height':'100%', 'border-radius':'5px', 'background':'#353C56'}),
                            html.Div([
                                html.I(className="bi bi-check-circle-fill",style={'font-size':'108px', 'color':'#2AAB69'}),
                                html.P("PASS",style={'color':'white', 'margin-top': '-20px', 'font-size': '24px'}),
                                html.Div([
                                    html.P("ความแม่นยำ",style={'color':'white', 'margin': '0px', 'font-size': '12px'}),
                                    html.P("98 %",style={'color':'white', 'margin': '0px', 'font-size': '24px'}),
                                ],style={'display':'flex','flex-direction':'column','justify-content':'center','align-items':'center', 'margin-bottom': '10px'}),
                                html.Button("ขอคำปรึกษาเพิ่มเติม",id="open_contact2",style={'width': '159px', 'height': '35px', 'color': 'white','border': '0px', 'background': '#7465F1', 'border-radius': '5px'}),
                            ],style={'display':'flex','flex-direction':'column','justify-content':'center', 'align-items':'center','width':'250px'})
                        ],style={'display':'flex','justify-content':'space-between','padding':'20px','background':'#292F45','width':'875px', 'height': '350px','border-radius': '5px', 'margin-right': '15px'})
                    ],style={'display':'flex','justify-content':'space-between','margin-left': '23px','margin-top':'15px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div(html.P("โมเดลอื่นที่ใช้",style={'color':'white', 'margin': '0px', 'font-size': '16px'}),style={'width':'25%'}),
                                html.Div(html.P("จำนวนฟีเจอร์ที่ใช้ในการเทรนด์",style={'color':'white', 'margin': '0px', 'font-size': '16px'}),style={'width':'47%'}),
                                html.Div(html.P("ความแม่นยำ",style={'color':'white', 'margin': '0px', 'font-size': '16px'}),style={'width':'14%'}),
                                html.Div(html.P("ความเร็ว",style={'color':'white', 'margin': '0px', 'font-size': '16px'}),style={'width':'14%'}),
                            ],style={'display':'flex','padding-left':'20px','padding-right':'20px','align-items':'center','justify-content':'space-between','background':'#353C56','width':'804px', 'height': '50px','border-radius': '5px 5px 0 0'}),
                            # other model
                            html.Div(otherModels, style={"overflow": "scroll",'height':'350px'})
                            
                        ],style={'background':'#292F45','width':'804px', 'height': '400px','border-radius': '5px', 'margin-right': '15px'}),
                        html.Div(style={'display':'flex','justify-content':'space-between','padding':'20px','background':'#292F45','width':'500px', 'height': '400px','border-radius': '5px', 'margin-right': '15px'})
                    ],style={'display':'flex','justify-content':'space-between','margin-left': '23px','margin-top':'15px', 'margin-bottom': '15px'})
                ]),
            ]
        ),
    ],
    style={'background':'#171D31'}
)

if __name__ == "__main__":
    app.run_server(debug=True)
