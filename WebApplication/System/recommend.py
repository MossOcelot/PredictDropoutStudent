from dash import Dash, Input, Output, State, html, dcc
import random

recommend_db = {'alert':[
    ("โปรดเช็คเกรดของตัวเองอีกครั้ง", 0.9),("ลองติดต่ออาจารย์ดูไหม",0.6), 
    ("ปีหน้าห้ามตกนะ", 0.5), ("โปรดพยายามมากกว่านี้", 0.5), ("ขยันให้มากๆ นะ", 0.5),
    # increase key

], 'lose':[
    ("โปรดติดต่ออาจารย์ด่วน", 0.8),
    # increase

], 'like':[
    ("เก่งจัง เลี้ยงข้าวเราหน่อย", 0.8),("เก่งจุง อิจฉาเลย", 0.8),
    ("พักมั้ง นะ", 0.7), ("กินไรทำไมเก่งจัง", 0.7), ("ปลอดภัย พยายามต่อไป", 0.5),
    ("เช็คอีกครั้งเพื่อผิดพลาด", 0.5), ("เก่งมาก พยายามต่อไป", 0.5), 
    # increase

], 'dislike':[
    ('ห้ามนอนดึกนะ', 0.5), ('อ่านหนังสือเยอะ', 0.9), ('อย่าเที่ยวเยอะเกิน', 0.5),
    # increase

]}

def getRecommend(label, percent):
    allrecommends = []
    if label == "R":
        status = ["alert", "lose", "dislike"]
        for s in status:
            for recom in recommend_db[s]:
                if percent >= recom[1]:
                    allrecommends.append([s, recom[0]])
                    
    else:
        status = ["like", "dislike"]
        for s in status:
            for recom in recommend_db[s]:
                if percent >= recom[1]:
                    allrecommends.append([s, recom[0]])
                    
    return allrecommends

def randomRecommend(label, percent):
    randList = getRecommend(label, percent)
    recommendList = random.choices(randList, k=6)

    return recommendList

icon_colors = {'alert':('bi bi-exclamation-diamond-fill', '#F8A22A'), 'lose':('bi bi-x-circle', '#E15354'),
               'like':('bi bi-hand-thumbs-up-fill', '#2AAB69'), 'dislike':('bi bi-hand-thumbs-down-fill', '#7465F1')}

def createRecommendCard(label, percent):
    randList = randomRecommend(label, percent)
    recommendCards = []

    for datas in randList:
        ic = icon_colors[datas[0]]
        print(ic[0], ic[1], datas[0], datas[1])
        recommendCards.append(html.Div([
                html.I(className=ic[0], style={'font-size':'56px', 'color':ic[1]}),
                html.P(datas[1],style={'color':'white', 'margin': '0px', 'font-size': '16px','margin-left':'8px'})
            ],style={'display':'flex','align-items':'center','height':'80px', 'background':'#353C56','border-radius':'5px','padding':'20px','margin-right':'24px', 'margin-top':'15px'}),
        )
    return recommendCards


