# Classe recuperata da DENOTER e modificata
#

from operator import itemgetter
import os

all_attr = open("attributes.txt", 'r')
all_attributes = []
for l in all_attr:
    app = l.split(":")
    all_attributes.append([app[0],(int)(app[1].strip())])

all_attributes = sorted(all_attributes, key=itemgetter(1), reverse=True)
print("a")





class Property:
    name = ""
    prob = 0.0
    nItem = 0

    def __init__(self, name, prob, nItem):
        self.name = name
        self.prob = prob
        self.nItem = nItem

def getProperties(file):
    l_t = []
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
                l_t.append(line.split(':')[0])

    list_negative = []
    for n in all_attributes:
        if (n[0] not in l_t) and (n[0] not in list_rigid):
            list_negative.append(n)

    return list_rigid, list_typical, nCanzoni, list_negative

def createFileForCocos(head, modifier):
    list_head_rigid, list_head_typical, nCanzoniHead, list_head_negative = getProperties('./genres/' + head)
    list_modifier_rigid, list_modifier_typical, nCanzoniModifier, list_modifier_negative = getProperties('./genres/' + modifier)
    list_modifier_typical = list_modifier_typical[:6]
    list_head_typical = list_head_typical[:6]
    head = head.replace(".txt", "")
    modifier = modifier.replace(".txt", "")
    print(head, modifier)


    f = open("prototipi/" + head + "_" + modifier, "w")
    f.write("#Title composizione\n")
    f.write("Title : " + head + "#" + modifier + "\n\n")
    f.write("#Concetto Principale\n")
    f.write("Head Concept Name : " + head +"\n")
    f.write("Head Concept Count : " + str(nCanzoniHead)  + "\n\n")
    f.write("#Concetto Modificatore\n")
    f.write("Modifier Concept Name : " + modifier + "\n")
    f.write("Modifier Concept Count : " + str(nCanzoniModifier)  + "\n\n")

    # Propriet?? Dure -
    for p in list_head_rigid:
        f.write("head, " + p + "\n")
    f.write("\n\n")

    for p in list_modifier_rigid:
        f.write("modifier, " + p + "\n")
    f.write("\n\n")





    # Properiet?? Deboli
    for n in list_modifier_negative[:2]:
        f.write("T(modifier), " + "-"+n[0] + ", " + '0.9' +", "+ str(nCanzoniModifier)+ "\n")

    for i in range(len(list_modifier_typical)):
        f.write("T(modifier), " + list_modifier_typical[i].name + ", " + str(list_modifier_typical[i].prob) +", "+ str(list_modifier_typical[i].nItem)+ "\n")
    f.write("\n")

    for n in list_head_negative[:2]:
        f.write("T(head), " + "-"+n[0] + ", " + '0.9' +", "+ str(nCanzoniHead)+ "\n")
    for i in range(len(list_head_typical)):
        f.write("T(head), " + list_head_typical[i].name + ", " + str(list_head_typical[i].prob) + ", "+str(list_head_typical[i].nItem) +"\n")
    f.write("\n")
    f.close()


# Main : lettura generi da associare creativamente tramite argomento di linea di comando, lettura propriet?? dai file, scrittura file per COCOS
if __name__ == '__main__':
    file_list = os.listdir('./genres')
    for file in file_list:
        for file2 in file_list:
            if file != file2:
                createFileForCocos(file, file2)
