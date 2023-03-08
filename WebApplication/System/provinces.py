province_db = ['ตรัง', 'ระนอง', 'สงขลา', 'ยะลา', 'สตูล', 'สุราษฎร์ธานี', 'ภูเก็ต',
       'พังงา', 'นครศรีธรรมราช', 'ปัตตานี', 'กระบี่', 'ชุมพร',
       'กรุงเทพมหานคร', 'พัทลุง', 'นราธิวาส', 'เชียงใหม่', 'สมุทรปราการ',
       'นนทบุรี', 'นครสวรรค์', 'ประจวบคีรีขันธ์', 'ชัยนาท', 'พะเยา',
       'นครปฐม', 'นครราชสีมา', 'สุพรรณบุรี', 'สระบุรี', 'ลพบุรี',
       'สมุทรสาคร', 'เชียงราย', 'พระนครศรีอยุธยา', 'กาญจนบุรี',
       'ฉะเชิงเทรา', 'เพชรบูรณ์', 'ขอนแก่น', 'ราชบุรี', 'ปราจีนบุรี',
       'ระยอง', 'กาฬสินธุ์', 'กําแพงเพชร', 'อื่นๆ', 'อุบลราชธานี',
       'ชัยภูมิ', 'ลำปาง', 'สกลนคร', 'มหาสารคาม', 'แพร่', 'ตาก', 'ลำพูน',
       'พิษณุโลก', 'พิจิตร', 'สุรินทร์', 'นครพนม', 'อุตรดิตถ์',
       'ปทุมธานี', 'จันทบุรี', 'หนองบัวลําภู', 'ชลบุรี', 'เลย', 'นครนายก',
       'หนองคาย', 'สมุทรสงคราม', 'ร้อยเอ็ด', 'อุดรธานี', 'สระแก้ว',
       'ยโสธร', 'อุทัยธานี', 'เพชรบุรี', 'ตราด', 'กำแพงเพชร', 'อ่างทอง',
       'สุโขทัย', 'บึงกาฬ']

province_id_db = [53., 61., 62., 60., 63., 64., 59., 57., 54., 56., 51., 52.,  1.,
       58., 55., 13., 50.,  3., 15., 67.,  2., 26., 66., 31., 72.,  7.,
        6., 71., 12.,  5., 65., 44., 19., 28., 69., 48., 49., 27., 11.,
        0., 41., 29., 22., 37., 33., 20., 14., 23., 18., 17., 38., 30.,
       25.,  4., 43., 76., 45., 35., 47., 39., 70., 34., 40., 74., 42.,
       10., 68., 46.,  9., 24., 78.]

def getProvinceDB():
    return province_db

def checkProvinceID(item):
    n = province_db.index(item)
    province_id = province_id_db[n]
    return province_id

