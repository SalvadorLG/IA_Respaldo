import random
import math
import copy
import numpy as np
import matplotlib.pyplot as plt

mejores_y = []

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

def Decimal(num):
    valor = int("".join(str(x) for x in num), 2)
    return valor

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
        
def crearPoblacion(poblacion, tamIndiv):
    b = 0
    listaIndividuos = []
    
    while(b < poblacion):
        lista = []
        for i in range(tamIndiv):
            num = random.randrange(0, 2)
            lista.append(num)
            
        bandera = Validar(lista)
        if(bandera == True):
            listaIndividuos.append(lista)
            b = b + 1
            
    return listaIndividuos

def CalcularY(X, A, B):
    
    respuesta = round((math.cos(A * X))*(math.sin(B * X)), 4)
    return respuesta

def CalcularFitness(ValoresAB, x, y, numDatos):
    global mejores_y
    
    cont = 0
    fitnesslista = []
    while(cont < len(ValoresAB)):
        fitnss = 0
        mejores_y.clear()
        for k in range (numDatos):
            xTemp = x[k]
            yTemp = y[k]
            
            respuesta = CalcularY(xTemp, ValoresAB[cont], ValoresAB[cont + 1])
            mejores_y.append(respuesta)
            
            fitnss = round(fitnss + abs((yTemp) - (respuesta)), 4)
            #print("<<<<<<<<<<",fitnss)
        fitnesslista.append(fitnss)
        #print(respuesta)
        cont = cont + 2
    return fitnesslista

def SumadorDeLista(listaNumeros):
    laSuma = 0
    for i in range(len(listaNumeros)):
        laSuma = laSuma + listaNumeros[i]
    return laSuma

def Ruleta(Fitness, numCombinaciones):
    FitnessMaximo = SumadorDeLista(Fitness)
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
    
#def MejoresCasos():

def Cruza(individuoA, individuoB):
    
    cruzaPntA = random.randrange(0,5)
    cruzaPntB = random.randrange(5,9)
    #print('\n',cruzaPntA,"-->",cruzaPntB)
    for cruzaPntA in range (cruzaPntB):
        temp = individuoA[cruzaPntA]
        individuoA[cruzaPntA] = individuoB[cruzaPntA]
        individuoB[cruzaPntA] = temp
        
    return individuoA, individuoB

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
        
    #print('\nMutacion\n',listaIndividuos)
def ObtenerMejores(Fitness, listaIndividuos):
    for numPasada in range(len(Fitness)-1,0,-1):
        for i in range(numPasada):
            if (Fitness[i]>Fitness[i+1]):
                tempFit = Fitness[i]
                Fitness[i] = Fitness[i+1]
                Fitness[i+1] = tempFit
                
                tempList = listaIndividuos[i]
                listaIndividuos[i] = listaIndividuos[i+1]
                listaIndividuos[i+1] = tempList
                
    if(len(listaIndividuos) > 10):
        tam = int(len(Fitness)/2)
        listaNueva = listaIndividuos[:tam]
        listaFitNueva = Fitness[:tam]
    elif(len(listaIndividuos) == 10):
        listaNueva = listaIndividuos
        listaFitNueva = Fitness
        
    listaFail = Fitness[len(Fitness) - 1]
    media = round((SumadorDeLista(Fitness)/len(Fitness)), 4)
    
    #print('MejoresFit',listaFitNueva,'\n')
    #print('Media ==>', media)
    #print('Peor ==>', listaFail)
    print(listaNueva[0])
    
    
    return listaFitNueva, listaNueva, listaFail, media
    

def Inicio(poblacion, tamIndiv, numDatos, x, y, Generaciones):
    
    MejorResultado = []
    Media = []
    PeorResultado = []
    MaxGeneracion = 0
    FitnessAnterior = []
    listaFail = []
    
    listaIndividuos = crearPoblacion(poblacion, tamIndiv)
    
    while(MaxGeneracion < Generaciones):
        
        #print(listaIndividuos)
        ValoresAB = BuscarAB(listaIndividuos)
        #print(ValoresAB)
        Fitness = CalcularFitness(ValoresAB, x, y, numDatos)
        #print('\nFitness\n',Fitness)
        #media = round((SumadorDeLista(Fitness)/len(Fitness)), 4)
        #Media.append(media)
        #print('\n ==<',media)
        
        while True:
        
            temporal = copy.copy(listaIndividuos)
            #print(temporal)
            combinaciones = Ruleta(Fitness, len(ValoresAB))
            #print(combinaciones)
            
            Hijos = []
            Cruzados = []
            cont = 0
            
            while(cont < (len(combinaciones))):
                CA = combinaciones[cont]
                CB = combinaciones[cont+1]
                
                individuoA, individuoB = Cruza(temporal[CA], temporal[CB])
                temporal[CA] = individuoA
                temporal[CB] = individuoB
                cont = cont + 2
                
            Cruzados = copy.copy(temporal)
            
            #print(Cruzados)
            
            contador = 0
            while(contador < (len(Cruzados))):
                individuo, valido = Mutacion(Cruzados[contador])
                if(valido == True):
                    Hijos.append(individuo)
                else:
                    Hijos.clear()
                contador = contador + 1
            
            #print(len(Hijos))
            
            if(len(Hijos) == poblacion):
                break
                
        #print("MUTACION")
        #print(Hijos)
        
        if(len(FitnessAnterior) == 0):
            FitnessAnterior = copy.copy(Fitness)
            PeorResultado.append(Fitness[len(Fitness)-1])
            media = round((SumadorDeLista(Fitness)/len(Fitness)), 4)
            #print('Media: ',media)
            Media.append(media)
        else:
            Fitness.extend(FitnessAnterior)
            listaIndividuos.extend(Hijos)
            print('\nAntes\n',listaIndividuos)
            Fitness, listaIndividuos, listaFail, media = ObtenerMejores(Fitness, listaIndividuos)
            PeorResultado.append(listaFail)
            print('\nDespues\n',listaIndividuos)
            #med = round((SumadorDeLista(FitnessAnterior)/len(FitnessAnterior)), 4)
            Media.append(media)
        
        #Media.append(round((SumadorDeLista(Fitness)/len(Fitness)), 4))
        
        MaxGeneracion = MaxGeneracion + 1
        
        

    global mejores_y
    print('Mejores Y\n',mejores_y,'\n')
    print('MejorResultado\n',Fitness,'\n')
    print('Media\n',Media,'\n')
    print('PeorResultado\n',PeorResultado,'\n')
    #plt.subplot(222)
    #plt.title("Fitnnes")
    #plt.plot(PeorResultado, linestyle='-', label = "peores")
    #plt.plot(Media,linestyle='-', label = "promedios")
    #plt.plot(Fitness,linestyle='-', label = "mejores")
    #plt.xlabel("generacion")  
    #plt.ylabel("cordenada") 
    #plt.legend()
   
    #plt.subplot(223)
    plt.title("valores reales y generados")
    plt.plot( x,y,linestyle='-', label = "original")
    plt.plot(x,mejores_y,linestyle='-', label = "generados")
    plt.xlabel("abscisa")  
    plt.ylabel("cordenada") 
    plt.legend()
    plt.show()
    
    
    

    
b = 0
poblacion = 10
tamIndiv = 12
listaIndividuos = []
numDatos = 21
Generaciones = 50

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

Inicio(poblacion, tamIndiv, numDatos, x, y, Generaciones)