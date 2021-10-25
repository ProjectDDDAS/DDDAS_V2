import Communication.nodoStationComunication as nodoStationComunication
import time

def main():
    #Inicialmente el nodo pide la informacion sobre que nodo es 
    numero_nodo, total_nodos, coordenadas_nodo = nodoStationComunication.solicitarNumeroNodo() # tener en cuenta caso Null, Null
    if numero_nodo == None:
        print('fallo buscando numero de nodo')
        return None
    print('Este es el nodo '+ str(numero_nodo))
    #Luego se solicitan las conexiones
    # se retorna una lista con el numero de los nodos a los que se tiene acceso, cada uno es un int 
    conexiones, betas = nodoStationComunication.solicitarConexiones(numero_nodo)
    if conexiones == None:
        print('fallo buscando conexiones')
        return None
    esperar = False
    #se espera hasta que el servidor autorice
    while esperar == False:
        esperar = nodoStationComunication.solicitarInicio(numero_nodo)
        print('Esperando autorizacion del station para empezar')
        time.sleep(3)

    
    print('\nEmpezo el algoritmo de consensus')
    #Ahora se implementa el algoritmo de consensus, se dan inicialmente 60 iteraciones
    for i in range(60):
        coordenadas_nodo = nodoStationComunication.solicitarUbicaciones(numero_nodo, betas, coordenadas_nodo)
        print(coordenadas_nodo)
        time.sleep(0.5)
    

main()

    


