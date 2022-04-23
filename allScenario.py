import numpy as np
import itertools
import copy
# leggo proprietà rigide e tipiche del prototipo
rigide = []
tipiche = []
index = 0
indexr = 0
f = open("try", "r")
for x in f:
  if x != "":
    app = x.replace("\n","").replace(" ","").split(",")
    if "T(modifier)" in x or "T(head)" in x:
      if app[1][0] == "-":
        app[1]=app[1][1:]
        app.append("-")
      else:
        app.append("+")
      app[2] = float(app[2])
      app.append(index)
      tipiche.append(app)
      index = index+1
    elif "modifier" in x or "head" in x:
      if app[1][0] == "-":
        app[1]=app[1][1:]
        app.append("-")
      else:
        app.append("+")
      app.append(indexr)
      rigide.append(app)
      indexr=indexr+1

print("rigide = ",rigide)
print("tipiche = ", tipiche)

# rileva conflitti
conflitti = {}
for r in rigide:
  if r[1] in conflitti.keys():
    conflitti[r[1]] = conflitti[r[1]]+[[r[3],"R"]]
  else:
    conflitti[r[1]] = [[r[3],"R"]]
for t in tipiche:
  if t[1] in conflitti.keys():
    conflitti[t[1]] = conflitti[t[1]] + [[t[4],"T"]]
  else:
    conflitti[t[1]] = [[t[4],"T"]]

print("conflitti = ", conflitti)

sempreZero = []
split = []
stop =0
for c in conflitti:
  index = conflitti[c]
  if len(index)>=2:
    # due proprietà rigide in conflitto tra loro
    if index[0][1] == "R" and index[1][1] == "R" :
      if rigide[index[0][0]][2] != rigide[index[1][0]][2]:
        print("conflitto tra rigide - NON COMPATIBILI")
        stop = 1
    # prima proprietà rigida e seconda tipica
    elif index[0][1] == "R" and index[1][1] == "T":
      sempreZero.append(index[1][0])
    # prima proprietà tipica e seconda rigida
    elif index[0][1] == "T" and index[1][1] == "R":
      sempreZero.append(index[0][0])
    # due proprietà tipiche in conflitto
    elif index[0][1] == "T" and index[1][1] == "T":
      # segno diverso
      if tipiche[index[0][0]][3] != tipiche[index[1][0]][3]:
        print("conflitto tra tipica-tipica, segno opposto")
        if tipiche[index[0][0]][0] == "T(modifier)" and tipiche[index[1][0]][0] == "T(head)":
          sempreZero.append(index[0][0])
      # stesso segno
      if tipiche[index[0][0]][3] == tipiche[index[1][0]][3]:
        print("conflitto tra tipica-tipica,stesso segno")
        split.append([index[0][0], index[1][0]])

print("sempre zero = ", sempreZero)
print("split = ", split)

propListIndexes = [ x for x in list(range(0, len(tipiche))) if x not in sempreZero]

for el in split:
  propListIndexes.remove(el[0])
  propListIndexes.remove(el[1])

print( "prop list indexes = ", propListIndexes)

allScenarios = list(map(list, itertools.product([0, 1], repeat=len(propListIndexes))))

maxScenari = 2**len(propListIndexes) * 3**len(split)

matrixScenarios = np.zeros((maxScenari, (len(tipiche))))

first = [0,1,0] * (int)(maxScenari/3)
second = [0,0,1] * (int)(maxScenari/3)
for s in split:
  matrixScenarios[:, s[0]] = first
  matrixScenarios[:, s[1]] = second

columns = []
for c in range(len(propListIndexes)):
  n = (int)((maxScenari)/(2**len(propListIndexes)))
  columns.append([item[c] for item in allScenarios] * n)

for index in propListIndexes:
  matrixScenarios[:, index] = columns.pop()

print("maxScenari = ", maxScenari)
print(matrixScenarios)




