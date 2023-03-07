campas = ['วิทยาเขตหาดใหญ่', 'วิทยาเขตภูเก็ต']
campas_id = ['01', '03']

def getCampas():
    return campas

def checkCampasID(item):
    n = campas.index(item)
    id = campas_id[n]
    return id

