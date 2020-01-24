# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 20:20:42 2020
@author: SalvadorLG
"""

import random
import math

listaGeneraciones = []
listaTempGeneraciones = []

def cruza(nuevaLista, combinaciones):
    
    conmCont = 0
    while(conmCont < len(combinaciones)):
        combA = combinaciones[conmCont]
        combB = combinaciones[conmCont+1]
        
        individuoA = nuevaLista[combA]
        individuoB = nuevaLista[combB]
        
        cruzaPntA = random.randrange(0,5)
        cruzaPntB = random.randrange(5,9)
    
        for cruzaPntA in range (cruzaPntB):
            temp = individuoA[cruzaPntA]
            individuoA[cruzaPntA] = individuoB[cruzaPntA]
            individuoB[cruzaPntA] = temp
            
            
        conmCont = conmCont + 2
        
    print('\n\nCruza\n',nuevaLista)
    return nuevaLista

def Mutacion(listaIndividuos, listaFitness):
    
    for i in range(len(listaIndividuos)):
        cromo = listaIndividuos[i]
        for j in range(len(cromo)):
            mutacionRandom = random.randrange(1,100)
            
            if(mutacionRandom <= 30):
                if(cromo[j] == 0):
                    cromo[j] = 1
                elif(cromo[j] == 1):
                    cromo[j] == 0
    
    print('\nMutacion\n',listaIndividuos)
    
    rechazados = 0
    rangoSeparacion = int((len(listaIndividuos[0])/2))
    listaAceptados = []
    
    Hijos = []
    HijosRechazados = []
     
    for i in range (len(listaIndividuos)):
        
        listatemp = listaIndividuos[i]
        
        ladoB = listatemp[rangoSeparacion:]
        ladoA = listatemp[:rangoSeparacion]
        
        a = int("".join(str(x) for x in ladoA), 2) 
        b = int("".join(str(x) for x in ladoB), 2)
        
        if(a > 0 and b > 0 and a < 60 and b < 60):
            listaAceptados.append(a)
            listaAceptados.append(b)
            print("A", ladoA, " --> ", str(a))
            print("B", ladoB, " --> ", str(b))
            Hijos.append(listatemp)
        else:
            rechazados = rechazados + 1
            HijosRechazados.append(listatemp)
            print("el individuo en la posicion ", str(i)," no cumple con los requisitos")
    
    print("Hijos\n",Hijos)
    
    
    if(rechazados > 0):
        print("Hijos Rechazados\n",HijosRechazados)
        combinaciones = Ruleta(listaFitness, HijosRechazados)
        print(combinaciones)
        cruzados = cruza(listaIndividuos, combinaciones)
        print('\n', cruzados)
        #Mutacion(cruzados, listaFitness)
        
    

def Ruleta(listaFitness, nuevaLista):
    
    suma = 0
    porcentaje = 0
    porcentajesLista = []
    combinaciones = []
    
    for i in range (len(listaFitness)):
        suma = round((suma + listaFitness[i]), 4)
    
    print(suma)
    
    for j in range (len(listaFitness)):
        porcentaje += round((listaFitness[j]/suma),4)
        porcentajesLista.append(round(porcentaje,4))
        
    #print(porcentajesLista)
    lenth = (len(nuevaLista) * 2)
    print("lenth: ",lenth)
    
    for k in range (lenth):
        rango = 0
        num = round(random.uniform(0, 1), 4)
        #print(num)
        for l in range (len(porcentajesLista)):
            if(num > rango and num <= porcentajesLista[l]):
                combinaciones.append(l)
                rango = porcentajesLista[l]
            rango = porcentajesLista[l]
            
    
    return combinaciones

def ValidarAceptados(listaIndividuos):
    
    rechazados = 0
    rangoSeparacion = int((len(listaIndividuos[0])/2))
    listaAceptados = []
    
    listaIndividuosTemp = []
    print(len(listaIndividuos))
    
    for i in range (len(listaIndividuos)):
        
        listatemp = listaIndividuos[i]
        
        ladoB = listatemp[rangoSeparacion:]
        ladoA = listatemp[:rangoSeparacion]
        
        a = int("".join(str(x) for x in ladoA), 2) 
        b = int("".join(str(x) for x in ladoB), 2)
        
        if(a > 0 and b > 0 and a < 60 and b < 60):
            valido = listatemp.copy()
            listaAceptados.append(a)
            listaAceptados.append(b)
            print("A", ladoA, " --> ", str(a))
            print("B", ladoB, " --> ", str(b))
            listaIndividuosTemp.append(valido)
        else:
            rechazados = rechazados + 1
            print("el individuo en la posicion ", str(i)," no cumple con los requisitos")
    
    
    if(rechazados > 0):
        print("rechazados", rechazados)
        tam = len(listaIndividuosTemp[0])
        extra = crearPoblacion(rechazados, tam)
        listaIndividuosTemp.extend(extra)
        return ValidarAceptados(listaIndividuosTemp)
    
    return listaAceptados, listaIndividuosTemp

def Fitness(listaIndividuos, numDatos, x, y):
    nuevaLista = []
    
    listaAceptados, nuevaLista = ValidarAceptados(listaIndividuos)
    
    for j in range (len(listaAceptados)):
        listaAceptados[j] = round((listaAceptados[j] * 0.1),2)
        
    print('\n',listaAceptados, '\n')
    #return listaFitness
    cont = 0
    fitnesslista = []
    while(cont < len(listaAceptados)):
        fitnss = 0
        for k in range (numDatos):
            xTemp = x[k]
            yTemp = y[k]
            respuesta = formula(xTemp, listaAceptados[cont], listaAceptados[cont + 1])
            fitnss = round(fitnss + abs((yTemp) - (respuesta)), 4)
            #print("<<<<<<<<<<",fitnss)
        fitnesslista.append(fitnss)
        #print(respuesta)
        cont = cont + 2
        
    return fitnesslista, nuevaLista

def formula(x,a,b):
    #A = a * x
    #print(a,"x",x,"=",A)
    #B = b * x
    #print(b,"x",x,"=",B)
    #print('\n',"cos ", math.cos(a * x))
    #print("sin ", math.sin(b * x))
    resultado = (math.cos(a * x))*(math.sin(b * x))
    #print(resultado)
    return resultado

def crearPoblacion(poblacion, tamIndiv):
    b = 0
    listaIndividuos = []
    
    while(b < poblacion):
        lista = []
        for i in range(tamIndiv):
            a = random.randrange(0, 2)
            lista.append(a)
        
        listaIndividuos.append(lista)
        b = b + 1
    return listaIndividuos
    
    
def Inicio(poblacion, tamIndiv, numDatos, x, y):
    listaIndividuos = crearPoblacion(poblacion, tamIndiv)
    
    listaFitness, nuevaLista = Fitness(listaIndividuos, numDatos, x, y)
    print(listaFitness)
    print("listaIndividuos\n",listaIndividuos)
    print("nuevaLista\n",nuevaLista)
    combinaciones = Ruleta(listaFitness, nuevaLista)
    #print(combinaciones)
    
    cruzados = cruza(nuevaLista, combinaciones)
    Mutacion(cruzados, listaFitness)
    
    print('\n\nFINALIZADO')

b = 0
poblacion = 10
tamIndiv = 12
listaIndividuos = []
numDatos = 21
x = [0.0000, 0.2500, 0.5000, 0.7500, 
     1.0000, 1.2500, 1.5000, 1.7500,
     2.0000, 2.2500, 2.5000, 2.7500,
     3.0000, 3.2500, 3.5000, 3.7500,
     4.0000, 4.2500, 4.5000, 4.7500,
     5.0000]

y = [0.0798, 0.8182, 0.5711, 0.0898,
     0.3947, 0.8480, 0.3564, -0.5355,
     -0.5669, -0.0071, -0.0745, -0.6289,
     -0.4354, 0.4901, 0.8266, 0.3052,
     0.1217, 0.6586, 0.7640, -0.0697, 
     -0.6862]

Inicio(poblacion, tamIndiv, numDatos, x, y)