#Converte de graus para int e vice-versa
def deg_to_int(deg:float):
    return int((4096*deg)/360)

def int_to_deg(val:int):
    return (360*val)/4096