from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas
import numpy
import time
from pycaret.classification import load_model, predict_model

from System.sendGmail import sendGmailToProfesser
from System.provinces import *
from System.campus import *
from System.majorDept import *
from System.recommend import createRecommendCard

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, 'assets/main.css'])

# model 
model = load_model("model/model_top_no_STILL_STUDENT_2Class_map_E_to_R_last_final")

IsFirstTime = True
oldConfirm = 0
predict_score = 0
predict_label = ''
recommendList = []
last_logout = 0
# Input Prediction
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks"), Input("confirm", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, n3, is_open):
    print(f'n1 {n1} n2 {n2} n3 {n3}')
    if n1 or n2 or n3:
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
x = ['1/1-1/2', '1/1-2/2', '1/1-3/2']
y = [69.19, 85.12, 93.21]

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
y = [100, 50, 170, 20]

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

# -------------------- Tap -------------------- 
@app.callback(
    [Output('my-output', 'children'),Output('alert-output', 'children')],
    [Input('my-tabs', 'value')] +
    [Input('confirm', 'n_clicks')] + 
    [Input(f'input-{i}', 'value') for i in range(1,16)],
)
def update_output(tab,confirm,*values):
    global predict_score
    global predict_label
    global IsFirstTime
    global oldConfirm

    if tab == 'tab-1':
        if '' not in values[:5]:
            return ["กรอกครบแล้ว",'']
        return ['ยังกรอกไม่ครบ','']
    elif tab == 'tab-2':
 
        if '' not in values and values.count(None) < 7:
       
            if confirm != oldConfirm:
    
                values = list(values)
                index_set = {
                    'MAJOR_ID': [checkMajorId(values[5])],
                    'DEPT_ID': [checkDeptId(values[6])],
                    'DEGREE_ID': [checkDegreeId(values[5])],
                    'STUD_BIRTH_PROVINCE_ID': [checkProvinceID(values[1])],
                    'INSTITUTION_PROVINCE_ID': [checkProvinceID(values[2])],
                    'ENG_SCORE': [values[3]],
                    'CAMPUS_ID': [checkCampasID(values[4])],
                    'เกรดปี1เทอม1': [values[7]],
                    'เกรดปี1เทอม2': [values[8]],
                    'เกรดปี2เทอม1': [values[9]],
                    'เกรดปี2เทอม2': [values[10]],
                    'เกรดปี3เทอม1': [values[11]],
                    'เกรดปี3เทอม2': [values[12]],
                    'เกรดปี4เทอม1': [values[13]],
                    'เกรดปี4เทอม2': [values[14]]
                }
                dataframe = pandas.DataFrame(index_set)
                # dataframe = dataframe.append(index_set, ignore_index=True)
                
                start,stop = dataframe.columns.tolist().index('เกรดปี1เทอม1'),dataframe.columns.tolist().index('เกรดปี4เทอม2') + 1
                print(f'{start}:{stop}')
                mean_row = (dataframe.iloc[0,start:stop]).sum() / (dataframe.iloc[0,start:stop] != 0).sum()
                print("mean : ",mean_row)
                data_1 = dataframe.iloc[0:1].replace(0,mean_row)
                #print(f'{data_1}')
                print("data_out",data_1)
                predict_value = predict_model(model, data_1)
                result = predict_value['prediction_label'][0]
                pre_score = predict_value['prediction_score'][0]
                predict_score = pre_score
                predict_label = result
                
                IsFirstTime = False
                oldConfirm = confirm
                if(result == "R"):
                    if sendGmailToProfesser("phuminsathipchan@gmail.com", f"{values[0]} มีโอกาสที่จะโดนรีไทร์", 
                                        f"""
รหัสนักศึกษา: {values[0]}
สถานะ: {result}
ความแม่นยำ: {pre_score * 100} %

หมายเหตุ: ข้อมูลข้างต้นเป็นเพียงการคาดการณ์เท่านั้นโปรดตรวจสอบอีกครั้ง
                                        """
                                        ):
                        print("successs")
                        return ['', '  เราได้ทำการส่งข้อมูลไปให้อาจารย์ที่ปรึกษาเรียบร้อยแล้ว  ']
                
                    return ['', '  การส่งแจ้งเตือนไปยังอาจารย์ที่ปรึกษามีปัญหา โปรดติดต่อได้ที่ >>>  ']
                
                
            return ["กรอกข้อมูลครบแล้ว กดยืนยันเพื่อพยากรณ์", '']
        return ['ยังกรอกข้อมูลไม่ครบ', '']
        
    else:
        return 'Error'

# -------------------- update dashboard -------------------- 
@app.callback(Output('output-div', 'children'),
              Input('interval-component', 'n_intervals'))
def update_output(n):
    if IsFirstTime:
        return html.Div([
            html.I(className="bi bi-question-circle-fill",style={'font-size':'108px', 'color':'#F8A22A'}),
            html.P("No Data",style={'color':'white', 'margin-top': '-20px', 'font-size': '24px'}),
            html.Div([
                html.P("ความแม่นยำ",style={'color':'white', 'margin': '0px', 'font-size': '12px'}),
                html.P("{:.2f} %".format(predict_score * 100),style={'color':'white', 'margin': '0px', 'font-size': '24px'}),
            ],style={'display':'flex','flex-direction':'column','justify-content':'center','align-items':'center', 'margin-bottom': '10px'}),
        ],style={'display':'flex','flex-direction':'column','justify-content':'center', 'align-items':'center','width':'250px'})
    else:
        if predict_label == 'G':
            return html.Div([
                html.I(className="bi bi-check-circle-fill",style={'font-size':'108px', 'color':'#2AAB69'}),
                html.P("PASS",style={'color':'white', 'margin-top': '-20px', 'font-size': '24px'}),
                html.Div([
                    html.P("ความแม่นยำ",style={'color':'white', 'margin': '0px', 'font-size': '12px'}),
                    html.P("{:.2f} %".format(predict_score * 100),style={'color':'white', 'margin': '0px', 'font-size': '24px'}),
                ],style={'display':'flex','flex-direction':'column','justify-content':'center','align-items':'center', 'margin-bottom': '10px'}),
            ],style={'display':'flex','flex-direction':'column','justify-content':'center', 'align-items':'center','width':'250px'})
    
        elif predict_label == 'R':
            return html.Div([
                html.I(className="bi bi-exclamation-circle-fill",style={'font-size':'108px', 'color':'#E15354'}),
                html.P("RETIRE",style={'color':'white', 'margin-top': '-20px', 'font-size': '24px'}),
                html.Div([
                    html.P("ความแม่นยำ",style={'color':'white', 'margin': '0px', 'font-size': '12px'}),
                    html.P("{:.2f} %".format(predict_score * 100),style={'color':'white', 'margin': '0px', 'font-size': '24px'}),
                ],style={'display':'flex','flex-direction':'column','justify-content':'center','align-items':'center', 'margin-bottom': '10px'}),
            ],style={'display':'flex','flex-direction':'column','justify-content':'center', 'align-items':'center','width':'250px'})

@app.callback(Output('output-layout1', 'children'),
              Input('interval-component-layout1', 'n_intervals'))
def update_output_layout1(n):
    if IsFirstTime:
        return html.Div([
                html.P('โปรดกรอกข้อมูลของคุณ',style={'color':'white','font-size':'16px','margin':'0px'}),
                html.P('เพื่อคาดการณ์โอกาสการตกออก',style={'color':'white','font-size':'12px','margin':'0px', 'margin-top':'10px'})
            ]),
    else:
        if predict_label == 'G':
            return html.Div([
                    html.P('ขอแสดงความยินดี',style={'color':'white','font-size':'16px','margin':'0px'}),
                    html.P('คุณยังไม่มีโอกาสโดนดรอป',style={'color':'white','font-size':'12px','margin':'0px', 'margin-top':'10px'})
                ]),
    
        elif predict_label == 'R':
            return html.Div([
                    html.P('โปรดระวัง',style={'color':'white','font-size':'16px','margin':'0px'}),
                    html.P('คุณมีโอกาสตกออก',style={'color':'white','font-size':'12px','margin':'0px', 'margin-top':'10px'})
                ]),

@app.callback(Output('output-layout1_2', 'children'),
              Input('interval-component-layout1_2', 'n_intervals'))
def update_output_layout1_2(n):
    if IsFirstTime:
        return html.I(className="bi bi-question-circle-fill",style={'font-size': '108px', 'color': '#F8A22A'})
    else:
        if predict_label == 'G':
            return html.I(className="bi bi-check-circle-fill",style={'font-size': '108px', 'color': '#2AAB69'})
        
        elif predict_label == 'R':
            return html.I(className="bi bi-exclamation-circle-fill",style={'font-size': '108px', 'color': '#E15354'})

@app.callback(Output('output-layout2', 'children'),
             [Input('interval-component-layout2', 'n_intervals'), Input('confirm', 'n_clicks') ])
def update_output_layout2(n,confirm):
    global recommendList
    global login_T
    #print(f"result: {predict_label} and {predict_score}")
    if (confirm != oldConfirm) & (login_T):
        login_T = 0
        time.sleep(1) # ทำให้ช้าลงเพื่อรอ data update
        recommendList = createRecommendCard(predict_label, predict_score)

    if IsFirstTime:
        return html.Div(html.P("ยังไม่มีข้อมูลพยากรณ์",style={'display':'flex','align-items':'center','justify-content':'center','height':'285px','color':'white', 'margin': '0px', 'font-size': '16px'}), style={'display':'grid', 'grid-template-columns':'562px','align-items':'center'})
    else:
        return html.Div(recommendList,style={'display':'grid', 'grid-template-columns':'281px 281px'})
    
@app.callback(Output('hidden-div','children'),[Input('user','value'),Input('pass','value')])
def login(user_name,pass_word):
    if (user_name in ["gao","moss","sun"]) & (str(pass_word) in ['123456',"123456","123456"]):
        print('test')
        #webbrowser.open('http://localhost:8050/')
        global IsFirstTime
        global oldConfirm
        global predict_score
        global predict_label
        global recommendList
        global login_T
        global last_logout
        global logouts
        login_T = 1
        last_logout = 0
        IsFirstTime = True
        oldConfirm = 0
        predict_score = 0
        predict_label = ''
        recommendList = []
        app.layout = layout
        return user_name+ str(pass_word)


    
app.layout = html.Div(children=[
html.Div(children=[html.H1(children='Login',style={"color":"white"}),
html.Div(children=[dcc.Input(id = 'user',type='text',placeholder="user",style={"textAlign": "center"})],style={"textAlign": "center","margin-top":"10px"}),
html.Div(children=[dcc.Input(id = 'pass',type='password',placeholder="password",style={"textAlign": "center"})],style={"textAlign": "center","margin-top":"10px"}),
html.Div(children=[dcc.Link(children=[html.Button("login",id = 'login',type="button")],href='/',refresh=True)],style={"textAlign": "center","margin-top":"10px"})
                        ],style={"textAlign": "center",'background':'#171D31',"position":"absolute","top":"40vh","left":"43vw"})
]+ [html.Div(id='hidden-div',style={"display":"none"})],style={"textAlign": "center","width":"100vw","height":"100vh",'background':'#171D31'})

@app.callback(Output('hiddens-div','children'),[Input('logout','n_clicks')])
def logout(logout):
    global last_logout
    global logouts
    logouts = logout
    print("test : ",logouts)
    print("test2 : ",last_logout)
    if(last_logout != logout):
        last_logout = logout
        #login_T = 0
        app.layout = html.Div(children=[
        html.Div(children=[html.H1(children='Login',style={"color":"white","margin-botton":""}),
        html.Div(children=[dcc.Input(id = 'user',type='text',placeholder="user",style={"textAlign": "center"})],style={"textAlign": "center","margin-top":"10px"}),
        html.Div(children=[dcc.Input(id = 'pass',type='password',placeholder="password",style={"textAlign": "center"})],style={"textAlign": "center","margin-top":"10px"}),
        html.Div(children=[dcc.Link(children=[html.Button("login",id = 'login',type="button")],href='/',refresh=True)],style={"textAlign": "center","margin-top":"10px"})
                        ],style={"textAlign": "center",'background':'#171D31',"position":"absolute","top":"39vh","left":"43vw"})
]+ [html.Div(id='hidden-div',style={"display":"none"})],style={"textAlign": "center","width":"100vw","height":"100vh",'background':'#171D31'})
    return 1


layout = html.Div( 
    [
        dbc.Row(
            [
                html.Div(id='result'),
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
                        dcc.Link(children=[html.Button("logout",id = 'logout',type="button",n_clicks=0,style={'width': '100px', 'height': '35px', 'color': 'white','border': '0px', 'background': '#7465F1', 'border-radius': '5px', 'margin-right': '10px'})],href='/',refresh=True),
                        html.Div(id="alert-output", style={'margin-right': '10px','height':'45px', 'background': '#F8A22A', 'color':'white', 'display':'flex','align-items':'center','justify-content':'center'}),
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
                                dcc.Interval(id='interval-component-layout1', interval=500, n_intervals=0),
                                html.Div(id='output-layout1'),
                                html.Div([
                                    html.P('มีนักศึกษาร้อยละ 20 ที่มีโอกาสตกออก',style={'color':'white','font-size':'14px','margin':'0px'}),
                                    html.Button("คาดการณ์",id='open',style={'width': '100px', 'height': '35px', 'color': 'white','border': '0px', 'background': '#7465F1', 'border-radius': '5px', 'margin-right': '36px', 'margin-top': '8px'}),
                                    # modal input predict
                                    dbc.Modal([
                                        dbc.ModalBody([
                                             dcc.Tabs(id='my-tabs', value='tab-1',
                                                children=[
                                                    dcc.Tab(label='ข้อมูล ม.ปลาย', value='tab-1',style={'background':'#292F45','border':'0','color':'white', 'font-size':'16'}, selected_style={'border':'0px','background':'#292F45',"border-bottom":"2px solid #7465F1","color": "#7465F1"}, children=[
                                                        html.Div([
                                                            html.P("รหัสนักศึกษา: ", className="plain_text"),
                                                            dcc.Input(id='input-1', type='text', value='', className="input_box")
                                                        ], className="box_in_Form"),
                                                        html.Div([
                                                            html.P("จังหวัดที่เกิด: ", className="plain_text"),
                                                            dcc.Dropdown(getProvinceDB(), getProvinceDB()[0], id='input-2',className="dropdown_box")
                                                        ], className="box_in_Form"),
                                                        html.Div([
                                                            html.P("จังหวัดของโรงเรียน: ",className="plain_text"),
                                                            dcc.Dropdown(getProvinceDB(), getProvinceDB()[0], id='input-3', className="dropdown_box")
                                                        ], className="box_in_Form"),
                                                        html.Div([
                                                            html.P("คะแนนภาษาอังกฤษ: ", className="plain_text"),
                                                            dcc.Input(id='input-4', type='number', value='', className="input_box")
                                                        ], className="box_in_Form"),
                                                        
                                                    ]),
                                                    dcc.Tab(label='ข้อมูล มหาลัย', value='tab-2' ,selected_style={'border':'0px','background':'#292F45',"border-bottom":"2px solid #7465F1","color": "#7465F1"}, children=[
                                                        html.Div([
                                                            html.P("วิทยาเขต: ", className="plain_text"),
                                                            dcc.Dropdown(getCampas(), getCampas()[0], id='input-5',className="dropdown_box")
                                                        ], className="box_in_Form"),
                                                        html.Div([
                                                                html.P("สาขาวิชา: ",className="plain_text"),
                                                                dcc.Dropdown(getMajors(), getMajors()[0], id='input-6', className="dropdown_box")
                                                            ], className="box_in_Form"),
                                                        html.Div([
                                                            html.P("ภาควิชา: ",className="plain_text"),
                                                            dcc.Dropdown(getDepts(), getDepts()[0], id='input-7', className="dropdown_box")
                                                        ], className="box_in_Form"),
                                                        html.Div([
                                                            html.P("เกรดเฉลี่ย: ", className="plain_text"),
                                                            html.Div([
                                                                html.Div([
                                                                    html.P("ปี 1 เทอม 1", className="mini_text"),
                                                                    dcc.Input(id='input-8', type='number', value=0, min=0, max=4,className="miniinput_box_for_grade")
                                                                ]),
                                                                html.Div([
                                                                    html.P("ปี 1 เทอม 2", className="mini_text"),
                                                                    dcc.Input(id='input-9', type='number', value=0, min=0, max=4,className="miniinput_box_for_grade")
                                                                ]), 
                                                                html.Div([
                                                                    html.P("ปี 2 เทอม 1", className="mini_text"),
                                                                    dcc.Input(id='input-10', type='number', value=0, min=0, max=4,className="miniinput_box_for_grade")
                                                                ]),html.Div([
                                                                    html.P("ปี 2 เทอม 2", className="mini_text"),
                                                                    dcc.Input(id='input-11', type='number', value=0, min=0, max=4,className="miniinput_box_for_grade")
                                                                ]),
                                                                html.Div([
                                                                    html.P("ปี 3 เทอม 1", className="mini_text"),
                                                                    dcc.Input(id='input-12', type='number', value=0, min=0, max=4,className="miniinput_box_for_grade")
                                                                ]), 
                                                                html.Div([
                                                                    html.P("ปี 3 เทอม 2", className="mini_text"),
                                                                    dcc.Input(id='input-13', type='number', value=0, min=0, max=4,className="miniinput_box_for_grade")
                                                                ]),html.Div([
                                                                    html.P("ปี 4 เทอม 1", className="mini_text"),
                                                                    dcc.Input(id='input-14', type='number', value=0, min=0, max=4,className="miniinput_box_for_grade")
                                                                ]),
                                                                html.Div([
                                                                    html.P("ปี 4 เทอม 2", className="mini_text"),
                                                                    dcc.Input(id='input-15', type='number', value=0, min=0, max=4,className="miniinput_box_for_grade")
                                                                ]), 
                                                            ],style={'display':'grid','grid-gap': '10px','justify-content': 'space-between', 'grid-template-columns': '1fr 1fr 1fr', 'grid-template-rows': '1fr 1fr 1fr'})
                                                        ])

                                                    ], style={'background':'#292F45','border':'0', 'color':'white', 'font-size':'16px'})
                                                ],style={'display':'flex','align-items':'center'}
                                            ),
                                            html.Div(id='my-output',style={'color':'#F8A22A'}),
                                            html.Div([
                                                dbc.Button(
                                                    "Close", id="close", className="button_cancle", n_clicks=0
                                                ),
                                                dbc.Button(
                                                    "Confirm", id="confirm", className="button_cancle", n_clicks=0
                                                )
                                            ],style={'display':'flex', 'justify-content':'space-between'})
                                        ], style={'background':'#292F45', 'border-radius': '5px'}),
                                    ],
                                    id="modal",
                                    is_open=False,),
                                ])
                            ],style={'display':'grid','align-content':'space-between','height': '143px',} ),
                            dcc.Interval(id='interval-component-layout1_2', interval=500, n_intervals=0),
                            html.Div(id='output-layout1_2'),

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
                                ], style={'display': 'flex'})
                            ], style={'display': 'flex', 'justify-content': 'space-between','margin-top':'10px'}),
                        ],style={'padding':'20px','background':'#292F45','width':'875px', 'height': '183px','border-radius': '5px', 'margin-right': '15px'})
                    ],style={'display':'flex','justify-content':'space-between','margin-left': '23px','margin-top':'15px'}),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.P("ความแม่นยำ",style={'color':'white', 'margin': '0px', 'font-size': '16px'}),
                                    html.P("95.30 %",style={'color':'white', 'margin': '0px', 'font-size': '24px'}),
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
                                # recommend box
                                dcc.Interval(id='interval-component-layout2', interval=500, n_intervals=0),
                                html.Div(id='output-layout2'),
                            ]),
                            html.Div(style={'width':'3px', 'height':'100%', 'border-radius':'5px', 'background':'#353C56'}),
                            ###
                            html.Div([
                                dcc.Interval(id='interval-component', interval=500, n_intervals=0),
                                html.Div(id='output-div'),
                                
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
    ] + [html.Div(id='hiddens-div',style={"display":"none"})],
    style={'background':'#171D31'}
)

app.css.append_css({
    "external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
})

if __name__ == "__main__":
    app.run_server(debug=False,port = 8051)
