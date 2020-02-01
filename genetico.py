# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:37:26 2020

@author: SalvadorLG
"""

#LIBRERIAS IMPORRTADAS
import random
import math
import copy
import numpy as np
import matplotlib.pyplot as plt

#VARIABLES GLOBALES QUE SIRVEN PARA GUARDAR TODOS LOS MEJORES CASOS
mejores_cromos = []
#mejores_ys = []
mejores_ys_individuos = []
Geberaciones = []
mejores_fitness = []
medias_fitness = []
peores_fitness = []

#FUNCION QUE COMBIERTE UNA LISTA CON 0s, Y 1s EN UN NUMERO DECIMAL
def Decimal(num):
    valor = int("".join(str(x) for x in num), 2)
    return valor

#FUNCION QUE VALIDA LOS DATOS DE UN INDIVIDUO AL PARTIRLO EN 2 Y OBTENER SU A Y B
#VERIFICA QUE LOS VALORES DE A Y B NO SE PASEN DE 59 Y SEAN MAYORES A 0
def Validar(individuo):
    rangoSeparacion = int((len(individuo)/2))
    ladoB = individuo[rangoSeparacion:]
    ladoA = individuo[:rangoSeparacion]
    a = Decimal(ladoA) 
    b = Decimal(ladoB)
    
    if(a > 0 and b > 0 and a < 60 and b < 60):
        #print("A", ladoA, " --> ", str(a))
        #print("B", ladoB, " --> ", str(b))
        return True
    else:
        #print("El individuo no cumple con los requisitos")
        return False
        
#FUNCION ENCARGADA DE CREAR LA POBLACION INICIAL
def crearPoblacion(poblacion, tamIndiv):
    b = 0
    creados = []
    
    while(b < poblacion):
        lista = []
        for i in range(tamIndiv):
            num = random.randrange(0, 2)
            lista.append(num)
            
        bandera = Validar(lista)
        if(bandera == True):
            creados.append(lista)
            b = b + 1
            
    return creados

# ESTA FUNCION SEPARA LOS INDIVIDUOS INDIVIDUALMENTE PARA OBTENER LOS VALORES DE A Y B
# Y LOS ENVIA A LA FUNCION Decimal() PARA CONVERTIRLOS EN DECIMALES, LOS MULTIPLICA POR 0.1
# Y LOS RETORNA COVERTIDOS A FLOTANTES
def BuscarAB(listaIndividuos):
    rangoSeparacion = int((len(listaIndividuos[0])/2))
    ValoresAB = []
    for i in range(len(listaIndividuos)):
        individuo = listaIndividuos[i]
        ladoB = individuo[rangoSeparacion:]
        ladoA = individuo[:rangoSeparacion]
        a = Decimal(ladoA)
        ValoresAB.append(round((a * 0.1), 4))
        b = Decimal(ladoB)
        ValoresAB.append(round((b * 0.1), 4))
    return ValoresAB

#CALCULA LAS Y INDIVIDUALES DE CADA INDIVIDUALES DE CADA INDIVIDUO
def CalcularY(X, A, B):
    
    respuesta = round((np.cos(A * X))*(np.sin(B * X)), 4)
    return respuesta

# FUNCION DEL FITNESS, ESTA ES LA MAS IMPORTANTE
# CALCULA EL FITNESS DE CADA INDIVIDUO
# LAS Ys SE ENVIAN A LA FUNCION CalcularY() Y LUEGO SE SUMAN, EL TOTAL DE LA SUMA RESTA A LA Y DADA
# Y - SUMAS_Y_GENERADAS Y ESE ES EL FITNESS
# LAS Y GENERADAS SE GUARDAN PARA POR CADA GENERACION Y SEGUN EL FITNESS SE ELIGE A LAS MEJORES Ys
# SE GURADA LA POSICION DEL FITNESS MAS PEQUEÑO PARA SABER QUE INDIVIDUO, Y Ys SE USARAN, ASI COMO SUS
# RESPECTIVAS A Y B
def CalcularFitness(ValoresAB, x, y, numDatos):
    global mejores_fitness
    global medias_fitness
    global peores_fitness
    #global mejores_ys
    global mejores_ys_individuos
    mejores_ys_individuos.clear()
    cont = 0
    fitnesslista = []
    while(cont < len(ValoresAB)):
        fitnss = 0
        mejores_ys = []
        for k in range (numDatos):
            xTemp = x[k]
            yTemp = y[k]
            
            respuesta = CalcularY(xTemp, ValoresAB[cont], ValoresAB[cont + 1])
            fitnss = round(fitnss + abs((yTemp) - (respuesta)), 4)
            
            mejores_ys.append(round(np.cos(ValoresAB[cont] * xTemp)*np.sin(ValoresAB[cont+1] * xTemp), 4))
            #print("<<<<<<<<<<",fitnss)
        fitnesslista.append(fitnss)
        mejores_ys_individuos.append(mejores_ys)
        cont = cont + 2
    #print(mejores_ys_individuos)
    mejorFit = copy.copy(fitnesslista)
    mejorFit.sort()
    print('\nMejor Fitness: ',mejorFit[0])
    mejores_fitness.append(mejorFit[0])
    
    media = round(sum(mejorFit)/(len(mejorFit)), 4)
    print('\nMedia Fitness: ',media)
    medias_fitness.append(media)
    
    print('\nPeor Fitness',mejorFit[len(mejorFit)-1])
    peores_fitness.append(mejorFit[len(mejorFit)-1])
    
    #pos = fitnesslista.index(mejorFit[0])
    
    
    cont = fitnesslista.count(mejorFit[0])
    contador = 0
    for i in range(len(fitnesslista)):
        if(fitnesslista[i] == mejorFit[0]):
            #print(i)
            contador = contador + 1
            if(contador == cont):
                pos = i
                
    print('\nLa posicion del mejor es: ',pos)
    print('\n A - B', ValoresAB)
    bestABPos = (pos * 2)
    print('\n Mejores A - B', ValoresAB[bestABPos] ,' - ', ValoresAB[bestABPos+1])
    return fitnesslista, pos

# FUNCION DE LA RULETA
# ESTA FUNCION SE ENCARGA DE LA PROBABILIDAD DE CRUZA, USA 2 RANDOMS PARA SABER CON CUALES SE CRUZARAN
# Y CREA UNA LISTA CON LAS COMBINACIONES 
    
def Ruleta(Fitness, numCombinaciones):
    FitnessMaximo = sum(Fitness)
    #print(FitnessMaximo)
    porcentaje = 0
    porcentajesLista = []
    combinaciones = []
    
    for j in range (len(Fitness)):
        porcentaje += round((Fitness[j]/FitnessMaximo),4)
        porcentajesLista.append(round(porcentaje,4))
        
    #print(porcentajesLista)
    
    for k in range (numCombinaciones):
        rango = 0
        num = round(random.uniform(0, 1), 4)
        #print(num)
        for l in range (len(porcentajesLista)):
            if(num > rango and num <= porcentajesLista[l]):
                combinaciones.append(l)
                rango = porcentajesLista[l]
            rango = porcentajesLista[l]
    
    return combinaciones

#FUNCION DE CRUZA
#USO 2 NUMEROS RANDOMS PARA PARA SABER APRTIR DE QUE PUNTO ESTE COMENZARA A HACER LA CRUZA Y 
# Y DONDE TERMINRA
def Cruza(individuoA, individuoB):
    
    cruzaPntA = random.randrange(0,5)
    cruzaPntB = random.randrange(5,9)
    #print('\n',cruzaPntA,"-->",cruzaPntB)
    for cruzaPntA in range (cruzaPntB):
        temp = individuoA[cruzaPntA]
        individuoA[cruzaPntA] = individuoB[cruzaPntA]
        individuoB[cruzaPntA] = temp
        
    return individuoA, individuoB

# FUNCION DE MUTACION 
#USA UN NUMERO RANDOM DE ENTRE 1 Y 100, CON UN PROBABILIDAD DE 30% DE MUTACION
#RECORRE CADA POSICION DEL INDIVIDUO Y VERIFICA EL NUMERO RANDOM PARA SABER SI ESTE SE MUTARA O NO
# ADEMAS USA LA FUNCION VALIDAR PARA SABER SI LOS NUEVOS A Y B NO SE PASEN DEL 59 Y SEAN MAYORES A 0
def Mutacion(Individuo):
    
    for j in range(len(Individuo)):
        mutacionRandom = random.randrange(1,100)
        
        if(mutacionRandom <= 30):
            if(Individuo[j] == 0):
                Individuo[j] = 1
            elif(Individuo[j] == 1):
                Individuo[j] = 0
                
    bandera = Validar(Individuo)
    if(bandera == True):
        return Individuo, bandera
    else:
        return Individuo, bandera

# FUNCION QUE INICIA TODO EL PROCESO
# AQUI SE USAN LAS VARIABLES GLOBALES PARA RECUPERAR LOS DATOS QUE SE GUARDAN EN LAS FUNCIONES
# SE CREA UN WHILE PARA QUE EL PROCESO SE REPITA HASTA EL NUMERO DE GENERACIONES DESEADAS

def Inicio(poblacion, tamIndiv, numDatos, x, y, Generaciones):
    listaIndividuos = []
    MaxGeneracion = 0
    bandera = False
    global mejores_cromos
    global mejores_fitness
    global mejores_ys
    global medias_fitness
    global peores_fitness
    global mejores_ys_individuos
    
    while(MaxGeneracion < Generaciones):
        # CREA LA POBLACION INICIAL UNA SOLA VEZ, LOS HIJOS RESULTANTES SERAN LA NUEVA GENERACION
        if(bandera == False):
            listaIndividuos = copy.copy(crearPoblacion(poblacion, tamIndiv))
            bandera = True
            
        #RECUPERA LOS VALORES A Y B DE CADA INDIVIDUO
        ValoresAB = BuscarAB(listaIndividuos)
        #print(ValoresAB,'\n')
        
        #RECUPERA EL FITNESS INDIVIDUAL DE CADA INDIVIDUO ASI COMO LA POSICION DEL INDIVIDUO CON EL 
        #MEJOR FITNESS DE CADA GENERACION
        Fitness, pos = CalcularFitness(ValoresAB, x, y, numDatos)
        print(Fitness,'\n')
        #GUARDA EL MEJOR INDIVIDUO DE LA GENERACION ACTUAL
        MejorIndividuo = copy.copy(listaIndividuos[pos])
        #GUARDA LOS MEJORES INDIVIDUOS POR CADA GENERACION
        mejores_cromos.append(MejorIndividuo)
        #print(MejorIndividuo,'\n')
        #print('\n->',MaxGeneracion,'\n',listaIndividuos,'\n')
        
        #EN ESTE WHILE SE HACEN LAS CRUZAS Y MUTACIONES SEGUN LAS COMBINACIONES RESULTANTES
        #Y SE EJECUTA HASTA QUE RESULTEN EN LA CREACION DE 1O HIJOS NUEVOS QUE RESPETEN LA CONDICION
        #DE QUE SUS A Y B NO SOBREPASEN EL 59 Y SEAN MAYORES A 0
        while True:
            #COPIA LA LISTA DE INDIVIDUOS ORIGINAL 
            temporal = copy.copy(listaIndividuos)
            # RECUPERA LAS COMBINACIONES
            combinaciones = Ruleta(Fitness, len(ValoresAB))
            Hijos = []
            Cruzados = []
            cont = 0
            
            while(cont < (len(combinaciones))):
                #RECUPERA LAS POSICIONES DE LOS INDIVIDUOS QUE SE CRUZARAN
                CA = combinaciones[cont]
                CB = combinaciones[cont+1]
                #RECUPERA LOS INDIVIDUOS RECULTANTES DE LA CRUZA, SEGUN LOS INDIVIDUOS QUE SE ENVIARON
                #A LA FUNCION DE CRUZA
                individuoA, individuoB = Cruza(temporal[CA], temporal[CB])
                #REMPLAZA LOS INDIVIDUOS NUEVOS EN LAS POSICIONES CORRESPONDIENTES
                temporal[CA] = individuoA
                temporal[CB] = individuoB
                cont = cont + 2      
            
            #GUARDA LA LISTA DE INDIVIDUOS RESULTANTES DE LAS CRUZAS
            Cruzados = copy.copy(temporal)
            
            contador = 0
            while(contador < (len(Cruzados))):
                #RECUPERA EL INDIVIDUO GENERADO EN LA FUNCION DE MUTACION Y EL VALOR BOOLEANO
                #QUE INDICA SI ESTE ES VALIDO O NO (OSEA MAYOR A 0 Y MENOR A 59)
                
                individuo, valido = Mutacion(Cruzados[contador])
                #SI EL VALOR BOOLEANO ES VALIDO EL INDIVIUO SE GUARDA
                if(valido == True):
                    Hijos.append(individuo)
                contador = contador + 1
            #SI LA LISTA DE HIJOS NO ES IGUAL A LA POBLACION DESEADA LAS LISTAS PRINCIPALES SE LIMPIAN
            #Y SE REINICIA EL CICLO Y GENERA NUEVAS COMBINACIONES, CRUZAS Y MUTACIONES HASTA QUE 
            #LA CONDICION SE CUMPLA
            #SI LA CONDICION SE CUMPLE A LA LISTA DE HIJOS SE LE REMUEVE EL ULTIMO ELEMENTO DE LA LISTA
            #Y DESPUES SE LE AGREGA MEJOR INDIVIDUO DE LA GENERACION DE LOS PADRES
            #LA LISTA PRINCIPAL SE LIMPIA Y SE LE ASIGNA A LA NUEVA GENERACION RESULTANTE
            if(len(Hijos) == poblacion):
                Hijos.pop()
                #print('Ultimo',mejores_cromos[len(mejores_cromos)-1])
                Hijos.append(mejores_cromos[len(mejores_cromos)-1])
                listaIndividuos.clear()
                listaIndividuos = copy.copy(Hijos)
                break
            else:
                Hijos.clear()
                temporal.clear()
        #print('\ncombinaciones: \n',combinaciones)
        #print('\nCRUZA: \n',Cruzados)
        #print('\nMUTACION: \n',Hijos,'\n')
        
        MaxGeneracion = MaxGeneracion + 1
        
    #print('\nmejores_cromos\n', mejores_cromos)
    print('\nmejores_fitness',mejores_fitness)
    #print('\nmedias_fitness',medias_fitness)
    #print('\npeores_fitness',peores_fitness)
    #print('\nmejores_ys---x\n',mejores_ys_individuos)
    #print(pos)
    print('\nmejores_ys\n',mejores_ys_individuos[pos])
    
    #GRAFICA LOS MEJORES, PERORES Y MEDIA DE LOS FITNESS
    plt.subplot(222)
    plt.title("Fitnnes")
    plt.plot(peores_fitness, linestyle='-', label = "peores")
    plt.plot(medias_fitness,linestyle='-', label = "promedios")
    plt.plot(mejores_fitness,linestyle='-', label = "mejores")
    plt.xlabel("generacion")  
    plt.ylabel("cordenada") 
    plt.legend()
    
    #GRAFICA Xs, Ys y Ys RESULTANTES
    plt.subplot(223)
    plt.title("valores reales y generados")
    plt.plot( x,y,linestyle='-', label = "original")
    plt.plot(x,mejores_ys_individuos[pos],linestyle='-', label = "generados")
    plt.xlabel("abscisa")  
    plt.ylabel("cordenada") 
    plt.legend()
    plt.show()

#SOLO INICIALIZA LOS VALORES
    
b = 0
poblacion = 10
tamIndiv = 12
numDatos = 21
Generaciones = 50

x = [0.0000, 0.2500, 0.5000, 0.7500, 
     1.0000, 1.2500, 1.5000, 1.7500,
     2.0000, 2.2500, 2.5000, 2.7500,
     3.0000, 3.2500, 3.5000, 3.7500,
     4.0000, 4.2500, 4.5000, 4.7500,
     5.0000]

y = [0.0718, 0.8103, 0.5631, 0.0818, 0.3868, 0.8400, 0.3484, -0.5434, -0.5749, -0.0151, -0.0825, -0.6369, -0.4434, 0.4821, 0.8186, 0.2972, 0.1137, 0.6506, 0.7561, -0.0776, -0.6942]

#y = [0.0798, 0.8182, 0.5711, 0.0898,
 #    0.3947, 0.8480, 0.3564, -0.5355,
  #   -0.5669, -0.0071, -0.0745, -0.6289,
   #  -0.4354, 0.4901, 0.8266, 0.3052,
    # 0.1217, 0.6586, 0.7640, -0.0697, 
     #-0.6862]

Inicio(poblacion, tamIndiv, numDatos, x, y, Generaciones)