# Classe recuperata da DENOTER e modificata
#

import os

class Property:
    name = ""
    prob = 0.0

    def __init__(self, name, prob):
        self.name = name
        self.prob = prob


# Classe per lettura del file di un GENERE
class ReaderFileProperty:

    # Ritorna la lista delle proprietà tipiche dal file indicato
    def getProperties(self, path_file):
        prop_list = []

        # Lettura file
        with open(path_file) as f:
            self.input_lines = f.readlines()

        # Inserimento proprietà tipiche
        for p in self.input_lines:
            prop = p.split(':')
            prob = float(prop[1].strip())
            x = Property(prop[0], round(prob, 2))
            prop_list.append(x)
        return prop_list


# Funzione scrittura file di input per COCOS
def writeFile_COCOS(head, modifier, head_prop, modifier_prop):
    f = open("prototipi/" + head + "_" + modifier, "w")
    f.write("#Title composizione\n")
    f.write("Title : " + head + "-" + modifier + "\n\n")
    f.write("#Concetto Principale\n")
    f.write("Head Concept Name : " + head + "\n\n")
    f.write("#Concetto Modificatore\n")
    f.write("Modifier Concept Name : " + modifier + "\n\n")

    # Proprietà Dure - lettura dai file nella cartella genres_attr
    a = open("./genres_attr/" + head + ".txt", "r")
    for p in a:
        f.write("head, " + p)
    f.write("\n\n")

    a = open("./genres_attr/" + modifier + ".txt", "r")
    for p in a:
        f.write("modifier, " + p)
    f.write("\n\n")

    # Properietà Deboli
    for i in range(len(modifier_prop)):
        f.write("T(modifier), " + modifier_prop[i].name + ", " + str(modifier_prop[i].prob) + "\n")
    f.write("\n")

    for i in range(len(head_prop)):
        f.write("T(head), " + head_prop[i].name + ", " + str(head_prop[i].prob) + "\n")
    f.write("\n")
    f.close()


def getProperties(file):
    list_rigid = []
    list_typical = []
    f = open(file, 'r')
    cont = 0
    for line in f:
        if line.strip() != '' and cont == 0:
            list_rigid.append(line.strip())
        elif line.strip() == '':
            cont += 1
        else:
            p = Property(line.split(':')[0], float(str(line.split(':')[1]).strip().replace('\n', '')))
            list_typical.append(p)
    return list_rigid, list_typical


def createFileForCocos(head, modifier):
    list_head_rigid, list_head_typical = getProperties('./genres/' + head)
    list_modifier_rigid, list_modifier_typical = getProperties('./genres/' + modifier)
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
    f.write("Title : " + head + "-" + modifier + "\n\n")
    f.write("#Concetto Principale\n")
    f.write("Head Concept Name : " + head + "\n\n")
    f.write("#Concetto Modificatore\n")
    f.write("Modifier Concept Name : " + modifier + "\n\n")

    # Proprietà Dure -
    for p in list_head_rigid:
        prob = float(str(p.split(':')[1]).strip().replace('\n', ''))
    f.write("\n\n")

    for p in list_modifier_rigid:
        f.write("modifier, " + p + "\n")
    f.write("\n\n")

    # Properietà Deboli
    for i in range(len(list_modifier_typical)):
        if(list_modifier_typical[i].prob) >= 0.7:
            f.write("T(modifier), " + list_modifier_typical[i].name + ", " + str(list_modifier_typical[i].prob) + "\n")
    f.write("\n")

    for i in range(len(list_head_typical)):
        if (list_head_typical[i].prob) >= 0.7:
            f.write("T(head), " + list_head_typical[i].name + ", " + str(list_head_typical[i].prob) + "\n")
    f.write("\n")
    f.close()


# Main : lettura generi da associare creativamente tramite argomento di linea di comando, lettura proprietà dai file, scrittura file per COCOS
if __name__ == '__main__':
    file_list = os.listdir('./genres')
    for file in file_list:
        for file2 in file_list:
            if file != file2:
                createFileForCocos(file, file2)
