import numpy as np

def rename(X):
    for l in X:
        nature = l[0]
        if nature == "Arc de triomphe":
            l[0] = 0
        elif nature == "Arène ou théâtre antique":
            l[0] = 1
        elif nature == "Chapelle":
            l[0] = 2
        elif nature == "Château":
            l[0] = 3
        elif nature == "Eglise":
            l[0] = 4
        elif nature == "Fort, blockhaus, casemate":
            l[0] = 5
        elif nature == "Indifférenciée":
            l[0] = 6
        elif nature == "Industriel, agricole ou commercial":
            l[0] = 7
        elif nature == "Monument":
            l[0] = 8
        elif nature == "Moulin à vent":
            l[0] = 9
        elif nature == "Serre":
            l[0] = 10
        elif nature == "Silo":
            l[0] = 11
        elif nature == "Tour, donjon":
            l[0] = 12
        elif nature == "Tribune":
            l[0] = 13
            
        usage1 = l[1]
        if usage1 == "Agricole":
            l[1] = 0
        if usage1 == "Annexe":
            l[1] = 1
        if usage1 == "Commercial et services":
            l[1] = 2
        if usage1 == "Indifférencié":
            l[1] = 3
        if usage1 == "Industriel":
            l[1] = 4
        if usage1 == "Religieux":
            l[1] = 5
        if usage1 == "Résidentiel":
            l[1] = 6
        if usage1 == "Sportif":
            l[1] = 7
            
        leger = l[2]
        if leger == 'Non':
            l[2] = 0
        elif leger == 'Oui':
            l[2] = 1
            
        date_app = l[3]
        if date_app != None:
            l[3] = int(date_app[0:4])
        else:
            l[3] = 0