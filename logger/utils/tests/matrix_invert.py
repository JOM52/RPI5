#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pdb
from datetime import datetime

nbre_records = 30 * 24 * 60
nbre_sensors = 25

matrice_org = []
matrice_sorted = []
ligne = []
colonne = []

for i in range(nbre_records):
    ligne = [i for x in range(nbre_sensors)]
    matrice_org.append(ligne)

# for l in matrice_org:
#     print(l)
# print()

a = range(len(matrice_org[0]))

# pdb.set_trace()
t_start = datetime.now()
for i in range(len(matrice_org[0])):
    colonne = []
    for k in range(len(matrice_org)):
        colonne.append(matrice_org[k][i])
    matrice_sorted.append(colonne)
    
for l in matrice_sorted:
    print(l)
print()
    
elapsed = datetime.now() - t_start

for l in matrice_sorted:
    print(l)
print()

t_start = datetime.now()
for l in matrice_sorted:
    for x in l:
        if x == 10:
            l.remove(x)
# 
# for l in matrice_sorted:
#     print(l)
# print("\nElapsed:", elapsed, "\n")


for l in matrice_sorted:
    print(l)
print("\nElapsed:", elapsed, "\n")
                      
