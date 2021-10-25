import numpy as np


def mainConsensus(ubicaciones, betas, coordenadas_nodo):
    distancias, normas = calcularDistancias(ubicaciones, coordenadas_nodo)
    calculo_gradiente = calcularGradiente(betas, distancias, normas)
    nuevas_coordenadas = coordenadas_nodo + 0.1*calculo_gradiente
    return nuevas_coordenadas

def calcularDistancias(ubicaciones, coordenadas_nodo):
    distancias = []
    normas = []
    for ubicacion in range(len(ubicaciones)):
        distancias.append([])
        norma = 0
        for x in range(len(coordenadas_nodo)):
            valor = coordenadas_nodo[x] - ubicaciones[ubicacion][x]
            norma = norma + valor**2
            distancias[ubicacion].append(valor)
        distancias[ubicacion] = np.array(distancias[ubicacion])
        norma = np.sqrt(norma)
        normas.append(norma)
    return distancias, normas 

def calcularGradiente(betas, distancias, normas):
    calculo = np.array([0.0 for x in range(len(distancias[0]))])
    for i in range(len(normas)):
        calculo -= distancias[i] - (betas[i]*distancias[i]*np.exp(-(normas[i])/2 ))
    return calculo

