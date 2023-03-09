from dash import Dash, Input, Output, State, html, dcc
import random

recommend_db = {'alert':[
    ("โปรดเช็คเกรดของตัวเองอีกครั้ง", 0.9),("ลองติดต่ออาจารย์ดูไหม",0.6), 
    ("ปีหน้าห้ามตกนะ", 0.5), ("โปรดพยายามมากกว่านี้", 0.5), ("ขยันให้มากๆ นะ", 0.5),
    ("ต้องพยายามและอดทนมากๆ นะ", 0.6), ("ควรมีความมุ่งมั่นในการเรียนรู้", 0.5), ("ควรพัฒนาตนเองนะ", 0.7), 
    ("ควรวางแผนการเรียนรู้", 0.6), ("ขอให้คุณพยายามเต็มที่เพื่อประสบความสำเร็จ", 0.7), ("ต้องมีการจัดทำแผนการเรียนรู้", 0.6)
], 'lose':[
    ("โปรดติดต่ออาจารย์ด่วน", 0.8),("โปรดติดต่อเพื่อขอคำปรึกษา", 0.8),("โปรดติดต่ออาจารย์เพื่อสอบถาม", 0.6),("โปรดติดต่อเพื่อขอความช่วยเหลือ", 0.6),
    ("สอบถามคำถามเพิ่มเติมกับอาจารย์", 0.6), ("ติดตามข่าวสารและประชาสัมพันธ์ของวิทยาลัยหรือมหาวิทยาลัย", 0.5), ("ขอติดต่ออาจารย์เพื่อขอคำแนะนำ", 0.6), 
    ("ขอติดต่อเจ้าหน้าที่เพื่อแจ้งปัญหาทางการศึกษา", 0.5), ("ควรขอข้อมูลเพิ่มเติมเกี่ยวกับหลักสูตร", 0.5), ("ควรขอคำแนะนำเกี่ยวกับการใช้ชีวิตในวัยศึกษา", 0.5)
], 'like':[
    ("เก่งจัง เลี้ยงข้าวเราหน่อย", 0.8),("เก่งจุง อิจฉาเลย", 0.8),
    ("พักมั้ง นะ", 0.7), ("กินไรทำไมเก่งจัง", 0.7), ("ปลอดภัย พยายามต่อไป", 0.5),
    ("เช็คอีกครั้งเพื่อผิดพลาด", 0.5), ("เก่งมาก พยายามต่อไป", 0.6), ("ดีเลิศเลย", 0.7), 
    ("เจ๋งแจ๋วสุดจ๊าบ", 0.6), ("ทำได้ดีมากๆ", 0.6), ("มีความรับผดชอบดี", 0.5), ("เก่งไม่ซ้ำใครเลย", 0.6), 
    ("อย่างมืออาชีพ", 0.5)
], 'dislike':[
    ('ห้ามนอนดึกนะ', 0.5), ('อ่านหนังสือเยอะ', 0.9), ('อย่าเที่ยวเยอะเกิน', 0.5), ('อย่าเล่นแต่เกม', 0.6) , 
    ('หมั่นทบทวนบทเรียนนะ', 0.8), ('เล่นโซเชียลแต่พอดี', 0.6), ('ควรมีสมาธิในการเรียน', 0.7) , 
    ('ควรใช้เวลาว่างให้เป็นประโยชน์', 0.8), ('ควรเรียนรู้ทักษะใหม่ๆ', 0.6), ('อย่านอนหลับนานเกินไป', 0.5)
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


