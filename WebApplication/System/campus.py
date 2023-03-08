campas = ['วิทยาเขตหาดใหญ่', 'วิทยาเขตภูเก็ต']
campas_id = [1, 3]

def getCampas():
    return campas

def checkCampasID(item):
    n = campas.index(item)
    id = campas_id[n]
    return id

