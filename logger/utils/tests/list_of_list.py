#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pdb
from datetime import datetime

nbre_records = 10 * 24 * 60
nbre_sensors = 25

matrice = []
ligne = []
colonne = []
matrice_2 = []

for i in range(nbre_records):
    ligne = [i for x in range(nbre_sensors)]
    matrice.append(ligne)

# for l in matrice:
#     print(l)
# print()

a = range(len(matrice[0]))

t_start = datetime.now()

for i in range(len(matrice[0])):
    colonne = []
    for k in range(len(matrice)):
        colonne.append(matrice[k][i])
    matrice_2.append(colonne)
print(datetime.now() - t_start)

# for l in matrice_2:
#     print(l)

                       
