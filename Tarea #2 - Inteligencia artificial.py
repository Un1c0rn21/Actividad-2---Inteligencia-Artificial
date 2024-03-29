import random, sys, math

#En lugar de matrices seusan lisatas de listas

#Genera una matrix de distancias de nPuntos x nPuntos
def matrizdeDistancias(nPuntos, distanciaMaxima):
    matriz = [[0 for i in range(nPuntos)]for j in range(nPuntos)]
    
    for i in range(nPuntos):
        for j in range(i):
            matriz[i][j] = distanciaMaxima * random.random()
            matriz[j][i] = matriz[i][j]
        
    return matriz

#Elige un paso de un alimentador, teniendo en cuenta las distancias 
#en el gps y descartando los puntos ya visitados.
def eligePunto(dists, gpss, visitados):
    # se calcula la tabla de pesos de cada punto
    listaPesos = []
    disponibles = []
    actual = visitados [-1]
    
    #Influencia de cada valor (alfa: gps; beta: distancias)
    alfa = 1.0
    beta = 0.5
    
    #El parametro beta (peso de las distancias) es 0.5, alfa=1.0
    for i in range(len(dists)):
        if i not in visitados:
            gps = math.pow((1.0 + gpss[actual][i]),alfa)
            peso = math.pow(1.0/dists[actual][i], beta) * gps
            disponibles.append(i)
            listaPesos.append(peso)
            
    #Se elige aleatoriamente uno de los puntos disponibles,
    #teniendo en cuenta su peso relativo.
    valor = random.random() * sum(listaPesos)
    acumulado = 0.0
    i = -1
    while valor > acumulado:
        i += 1
        acumulado += listaPesos[i]
        
    return disponibles[i]


# Genera un alimentador que elegirá un camino reniendo en cuenta
#las distancias y los rastros del gps. devuelve una tupla con el camino y su longitud

def eligeCamino(distancias,rastro):
    #El punto inicial siempre es el A
    camino = [0]
    longCamino = 0
    
    #Elegir un camino según la distancia y el rastro del gps
    while len(camino) < len(distancias):
        punto = eligePunto(distancias, rastro, camino)
        longCamino += distancias[camino[-1]][punto]
        camino.append(punto)
        
    #Para terminar hay que volver al punto de origen (0)
    longCamino += distancias[camino[-1]][0]
    camino.append(0)
    
    return (camino, longCamino)

#Actualiza la matriz de feromonas siguiendo el camino recibido
def rastroGps(rastro, camino, dosis):
    for i in range(len(camino) - 1):
        rastro[camino[i]][camino[i+1]] += dosis
        
#Cuenta el rastro multiplicandolas por una constante
# = 0.9 (En otras palabras el coeficiente de conteo es 0.1)
def conteoRastro(rastro):
    for lista in rastro:
        for i in range(len(lista)):
            lista[i] *= 0.9
            
#Resuelve el problema del viajero a tra vez de los puntos
#mediante un algoritmo de la colonia de hormigas.
#recibe una matriz de distancias y devuelve una tupla con el mejor 
#camino que ha obtenido (lsita de indices) y su longitud
def alimentador(distancias, iteraciones, distMedia):
    #Primero se crea una matriz de rastro vacía
    n = len(distancias)
    rastro = [[0 for i in range(n)] for j in range(n)]
    
    #El mejor camino y su longitud (inicialmente "infinita")
    mejorCamino = []
    longMejorCamino = sys.maxsize
        
    #En cada iteración se genera un alimentador, que elige un camino,
    #y si es mejor que el mejor que se tenía, deja su rastro en 
    #el gps (mayor cuanto mas corto sea el camino)
    for iter in range(iteraciones):
        (camino, longCamino) = eligeCamino(distancias, rastro)
        
        if longCamino <= longMejorCamino:
            mejorCamino = camino
            longMejorCamino = longCamino
            
        rastroGps(rastro, camino, distMedia/longCamino)
        
        #En cualquier caso, los rastros del gps se van contando
        conteoRastro(rastro)
        
        
    #Se devuelve el mejro camino que haya encontrado
    return (mejorCamino, longMejorCamino)


#Generación de una matriz de prueba
numPuntos = 4
distanciaMaxima = 4
puntos = matrizdeDistancias(numPuntos, distanciaMaxima)

#Obtencion del mejor camino
iteraciones = 1000
distMedia = numPuntos*distanciaMaxima/2
(camino, longCamino) = alimentador(puntos, iteraciones, distMedia)
print("Camino: ",camino)
print("Longitud del camino: ", longCamino)
