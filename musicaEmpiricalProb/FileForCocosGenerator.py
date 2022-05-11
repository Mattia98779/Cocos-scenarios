# Classe recuperata da DENOTER e modificata
#

import os

class Property:
    name = ""
    prob = 0.0
    nItem = 0

    def __init__(self, name, prob, nItem):
        self.name = name
        self.prob = prob
        self.nItem = nItem

def getProperties(file):
    list_rigid = []
    list_typical = []
    f = open(file, 'r')
    cont = 0
    nCanzoni = 0
    for line in f:
        if "#Numero di canzoni:" in line:
            nCanzoni=int(str(line.split(':')[1]).strip().replace('\n', ''))
        else:
            if line.strip() != '' and cont == 0:
                list_rigid.append(line.strip())
            elif line.strip() == '':
                cont += 1
            else:
                p = Property(line.split(':')[0],
                             float(str(line.split(':')[1].split(",")[0]).strip().replace('\n', '')),
                             int(str(line.split(':')[1].split(",")[1]).strip().replace('\n', '')))
                list_typical.append(p)
    return list_rigid, list_typical, nCanzoni

def createFileForCocos(head, modifier):
    list_head_rigid, list_head_typical, nCanzoniHead = getProperties('./genres/' + head)
    list_modifier_rigid, list_modifier_typical, nCanzoniModifier = getProperties('./genres/' + modifier)
    list_modifier_typical = list_modifier_typical[:6]
    list_head_typical = list_head_typical[:6]
    head = head.replace(".txt", "")
    modifier = modifier.replace(".txt", "")
    print(list_head_rigid)
    print(list_head_typical)
    print()
    print(list_modifier_rigid)
    print(list_modifier_typical)
    print()
    print()

    f = open("prototipi/" + head + "_" + modifier, "w")
    f.write("#Title composizione\n")
    f.write("Title : " + head + "#" + modifier + "\n\n")
    f.write("#Concetto Principale\n")
    f.write("Head Concept Name : " + head +"\n")
    f.write("Head Concept Count : " + str(nCanzoniHead)  + "\n\n")
    f.write("#Concetto Modificatore\n")
    f.write("Modifier Concept Name : " + modifier + "\n")
    f.write("Modifier Concept Count : " + str(nCanzoniModifier)  + "\n\n")

    # Proprietà Dure -
    for p in list_head_rigid:
        f.write("head, " + p + "\n")
    f.write("\n\n")

    for p in list_modifier_rigid:
        f.write("modifier, " + p + "\n")
    f.write("\n\n")

    # Properietà Deboli
    for i in range(len(list_modifier_typical)):
        f.write("T(modifier), " + list_modifier_typical[i].name + ", " + str(list_modifier_typical[i].prob) +", "+ str(list_modifier_typical[i].nItem)+ "\n")
    f.write("\n")

    for i in range(len(list_head_typical)):
        f.write("T(head), " + list_head_typical[i].name + ", " + str(list_head_typical[i].prob) + ", "+str(list_head_typical[i].nItem) +"\n")
    f.write("\n")
    f.close()


# Main : lettura generi da associare creativamente tramite argomento di linea di comando, lettura proprietà dai file, scrittura file per COCOS
if __name__ == '__main__':
    file_list = os.listdir('./genres')
    for file in file_list:
        for file2 in file_list:
            if file != file2:
                createFileForCocos(file, file2)
