import numpy as np

def rename(X):
    for l in X:
        for i in range(6):
            nature = l[0+6*i]
            if nature == "Arc de triomphe":
                l[0+6*i] = 0
            elif nature == "Arène ou théâtre antique":
                l[0+6*i] = 1
            elif nature == "Chapelle":
                l[0+6*i] = 2
            elif nature == "Château":
                l[0+6*i] = 3
            elif nature == "Eglise":
                l[0+6*i] = 4
            elif nature == "Fort, blockhaus, casemate":
                l[0+6*i] = 5
            elif nature == "Indifférenciée":
                l[0+6*i] = 6
            elif nature == "Industriel, agricole ou commercial":
                l[0+6*i] = 7
            elif nature == "Monument":
                l[0+6*i] = 8
            elif nature == "Moulin à vent":
                l[0+6*i] = 9
            elif nature == "Serre":
                l[0+6*i] = 10
            elif nature == "Silo":
                l[0+6*i] = 11
            elif nature == "Tour, donjon":
                l[0+6*i] = 12
            elif nature == "Tribune":
                l[0+6*i] = 13
                
            usage1 = l[1+6*i]
            if usage1 == "Agricole":
                l[1+6*i] = 0
            if usage1 == "Annexe":
                l[1+6*i] = 1
            if usage1 == "Commercial et services":
                l[1+6*i] = 2
            if usage1 == "Indifférencié":
                l[1+6*i] = 3
            if usage1 == "Industriel":
                l[1+6*i] = 4
            if usage1 == "Religieux":
                l[1+6*i] = 5
            if usage1 == "Résidentiel":
                l[1+6*i] = 6
            if usage1 == "Sportif":
                l[1+6*i] = 7
                
            leger = l[2+6*i]
            if leger == 'Non':
                l[2+6*i] = 0
            elif leger == 'Oui':
                l[2+6*i] = 1
                
            date_app = l[3+6*i]
            if date_app != None:
                l[3+6*i] = int(date_app[0:4])
            else:
                l[3+6*i] = 0