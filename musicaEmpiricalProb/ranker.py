import os
class Canzone:
    def __init__(self, title, performer, g, attributes):
        self.title = title
        self.performer = performer
        self.genre = g
        self.attributes = attributes

class Prototipo:
    def __init__(self, name, rigide, tipiche):
        self.name = name
        self.rigide = rigide
        self.tipiche = tipiche

def leggiCanzone(path):
    f = open("./songs/" + path, "r")
    file_name = os.path.basename(path)
    datas = os.path.splitext(file_name)[0].split("#")
    attributes = {}
    for l in f:
        if l!="":
            line = l.split(":")
            line = [s.strip() for s in line]
            attributes[line[0]] = [line[1],line[2]]
    c = Canzone(datas[0],datas[1],datas[2],attributes)
    return c

def leggiPrototipo(path):
    name = ""
    rigide = []
    tipiche = []
    result= []
    index = 0
    indexr = 0
    nPropMod = 0
    totProp = 0
    nHead = 0
    nModifier = 0
    f = open("./prototipi/" + path, "r")
    for x in f:
        if x != "":
            if "Title :" in x:
                name= x.split(":")[1].strip().replace("\n","")
            if "Result :" in x :
                app=x.split(":")[1].split(",")[:-1]
                result = [int(s.replace("'","")) for s in app]
            else:
                app = x.replace("\n", "").split(",")
                app = [s.strip() for s in app]
                if "Head Concept Count :" in x:
                    nHead = int(x.split(":")[1])
                if "Modifier Concept Count :" in x:
                    nModifier = int(x.split(":")[1])
                if "T(modifier)" in x or "T(head)" in x:
                    totProp = totProp + 1
                    if "T(modifier)" in x:
                        nPropMod = nPropMod + 1
                    if app[1][0] == "-":
                        app[1] = app[1][1:]
                        app.append("-")
                    else:
                        app.append("+")
                    app[2] = float(app[2])
                    app[3] = int(app[3])
                    app.append(index)
                    tipiche.append(app)
                    index = index + 1
                elif "modifier" in x or "head" in x:
                    if app[1][0] == "-":
                        app[1] = app[1][1:]
                        app.append("-")
                    else:
                        app.append("+")
                    app.append(indexr)
                    rigide.append(app)
                    indexr = indexr + 1

    for i in range(len(result)-1,0, -1):
        if result[i]==0:
            tipiche.pop(i)

    prot = Prototipo(name,rigide,tipiche)
    return prot

def classifica(protipo, canzoni):
    classifica = []
    for c in canzoni:
        score = 1
        classifica.append([c, score])
    return classifica

if __name__ == '__main__':
    listaCanzoni = []
    listaPrototipi = []
    file_list = os.listdir('./songs')
    for file in file_list:
        listaCanzoni.append(leggiCanzone(file))
    print("FINE LETTURA CANZONI")
    file_list = os.listdir('./prototipi')
    for file in file_list:
        listaPrototipi.append(leggiPrototipo(file))
    print("FINE LETTURA PROTOTIPI")
    for p in listaPrototipi[:3]:
        classifica(p, listaCanzoni)
    print("!")
