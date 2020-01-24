# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 15:17:13 2020

@author: SalvadorLG
"""
import numpy as np

lista = [1,0,1,0,0,1]
lista1 = lista
print(lista)
print(lista1)

for i in range(len(lista1)):
    if(lista1[i] == 1):
        print('1',lista1[i])
        lista1[i] = 0
        print('2',lista1[i])
    elif(lista1[i] == 0):
        print('3',lista1[i])
        lista1[i] = 1
        print('4',lista1[i])

print(lista)
print(lista1)

x = np.array([0,1,0,1,1,0])
a = x

print(x)
print(a)