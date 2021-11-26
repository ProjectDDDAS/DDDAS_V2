import Communication.stationNodeComunication as stationNodeComunication
import numpy as np

def main():
    #definir cantidad de nodos
    print('Bienvenido al sistema de consensus de agentes\n')
    manual = input('Ingrese m si quiere definir las variables por consola, o d si quiere usar los valores por defecto: ')
    if manual =='m':
        total_agentes = int(input('Ingrese el numero de agentes que se van a manejar'))
        # definir grafo
        conexiones = definirConexionesConsola(total_agentes)
        # dado que se manejara una simulacion inicialmente es necesario definir posiciones iniciales para los agentes
        # iniciar servidor para comunicarce 
        ubicaciones = definirUbicacionesConsola(total_agentes)
        # Para implementar el algoritmo de consensus es necesario enviar la informacion de los valores de los betas obtenidos 
        # a partir de las distancias deseadas entre agentes
        distancias = definirDistancias(total_agentes, conexiones)
    else:
        total_agentes = 3
        conexiones = np.array([[0,1,1],
                                [1,0,1],
                                [1,1,0]])
        ubicaciones = [[1.0,0.0],
                        [2.2,4.5],
                        [3.1,6.1]]
        distancias = np.array([[0.0,4.0,4.0],
                                [4.0,0.0,4.0],
                                [4.0,4.0,0.0]])

    betas = calcularBetas(total_agentes,distancias)
    

    stationNodeComunication.empezarComunicacion(total_agentes, conexiones, ubicaciones, betas)

    


def definirConexionesConsola(total_agentes):
    conexiones = np.zeros((total_agentes, total_agentes))
    for i in range(total_agentes):
        asociados = input('Ingrese el numero de los agentes asociados al agente '+ str(i)+ ' en formato: x1,x2,x3: ')
        asociados_lista = asociados.split(',')
        asociados_lista = [int(x) for x in asociados_lista]
        for pos in asociados_lista:
            conexiones[i][pos] = 1
    return conexiones

def definirUbicacionesConsola(total_agentes):
    ubicaciones = []
    for agente in range(total_agentes):
        coordenadas = input('Ingrese las coordenadas asociadas al agente '+ str(agente)+ ' de la forma: x,y,z: ')
        coordenadas = coordenadas.split(',')
        coordenadas = [float(x) for x in coordenadas]
        ubicaciones.append(coordenadas)
    return ubicaciones

def definirDistancias(total_agentes, conexiones):
    distancias = np.zeros((total_agentes, total_agentes))
    for f in range(total_agentes):
        for c in range(total_agentes):
            if conexiones[f][c] == 1:
                distancia = float(input('ingrese la distancia deseada entre los agentes '+str(f)+' y '+ str(c)+ ': '))
                distancias[f][c] = distancia
    return distancias 


def calcularBetas(total_agentes, distancias):
    betas = np.zeros((total_agentes, total_agentes))
    for f in range(total_agentes):
        for c in range(total_agentes):
            if distancias[f][c] != 0:
                distancia = distancias[f][c]
                beta = 1/np.exp(-distancia/2)
                betas[f][c] = beta
    return betas



main()
