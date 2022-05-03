import numpy
import numpy as np
import itertools

# leggo proprietà rigide e tipiche del prototipo
rigide = []
tipiche = []
index = 0
indexr = 0
nPropMod = 0
totProp = 0
f = open("try", "r")
for x in f:
  if x != "":
    app = x.replace("\n","").replace(" ","").split(",")
    if "T(modifier)" in x or "T(head)" in x:
      totProp=totProp+1
      if "T(modifier)" in x:
        nPropMod=nPropMod+1
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
stop =0
generaTutto = 0
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
      # segno diverso
      if rigide[index[0][0]][2] != tipiche[index[1][0]][3]:
        print("conflitto tra rigida-tipica, segno opposto")
        sempreZero.append(index[1][0])
        if tipiche[index[1][0]][0] == "T(head)":
          generaTutto=1
      # stesso segno
      if rigide[index[0][0]][2] == tipiche[index[1][0]][3]:
        print("conflitto tra rigida-tipica,stesso segno")
    # prima proprietà tipica e seconda rigida
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

print("sempre zero = ", sempreZero)

propListIndexes = [ x for x in list(range(0, len(tipiche))) if x not in sempreZero]

print( "prop list indexes = ", propListIndexes)

propListIndexesModifier = []
propListIndexesHead = []

for i in propListIndexes:
  if tipiche[i][0] == "T(modifier)":
    propListIndexesModifier.append(i)
  else:
    propListIndexesHead.append(i)
print("propListIndexesHead = ", propListIndexesHead)
print("propListIndexesModifier = ", propListIndexesModifier)

allScenariosHead = list(map(list, itertools.product([0, 1], repeat=len(propListIndexesHead))))
allScenariosModifier = list(map(list, itertools.product([0, 1], repeat=len(propListIndexesModifier))))
if generaTutto==0:
  allScenariosHead.pop(-1)
allScenarios = []
for elHead in allScenariosHead:
  for elMod in allScenariosModifier:
    allScenarios.append(elHead+elMod)

maxScenari = len(allScenarios)

matrixScenarios = np.zeros((maxScenari, (len(tipiche))))

columns = []
for c in range(len(propListIndexes)):
  columns.append([item[c] for item in allScenarios] )

for index in propListIndexes:
  matrixScenarios[:, index] = columns.pop()

#print(matrixScenarios)

# aggiungo probabilità
prob = []
for r in matrixScenarios:
  p=1
  c=0
  for el in r:
    if el<0.5:
      p=p*(1-tipiche[c][2])
    else:
      p=p*tipiche[c][2]
    c=c+1
  prob.append([p])

matrixProb = numpy.append(matrixScenarios, prob, axis=1)
#print(matrixProb)
matrixProbOrdered = matrixProb[matrixProb[:,-1].argsort()]
np.set_printoptions(suppress=True)
print(matrixProbOrdered)