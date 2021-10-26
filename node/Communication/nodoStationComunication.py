import socket
import numpy as np
import Consensus.implementacionConsensus as implementacionConsensus
# este codigo se encarga de implementar las funciones para comunicar el nodo con la estacion
# La estacion sera el server, y el nodo el cliente
# El nodo le hace solicitudes a la estacion sobre:
# 1. Informacion sobre que numero que numero de nodo es, cuantos hay y su ubicacion inicial.
# 2. Informacion sobre con que nodos esta conectado, y tambien la distancia que se quiere con ellos 
# 3. Informacion de la ubicacion de los nodos a los que tiene acceso.
# 4. Informacion sobre cuando empezar a realizar el proceso de consensus
# 5. Finalizo el algoritmo de consensus
# En el caso de la solicitud 3, despues de recivir la informacion y hacer los calculos necesarios 
# para estimar su movimiento, debe devolverle al servidor su nueva ubicacion (esto solamente para 
# el caso de la simulacion dado que no podemos acceder a los datos de ubicaciones por medio de la camara)

global ip_station

#Asignar el numero de la ip de la estacion
ip_station = '192.168.0.101'


# dado que los mensajes son str, es necesario establecer convenciones para diferenciar os distintos tipos.
# Para mensaje 1, este sera 'N-?', esto indicara a la estacion que le debe asignar un numero a este nodo
# Para mensaje 2, este sera 'N#-connections', donde # sera el numero asignado al nodo
# Para mensaje 3, este sera 'N#-ubications', donde # sera el numero asignado al nodo
# Para mensaje 4, este sera 'N#-begin', donde # sera el numero asignado al nodo


def solicitarNumeroNodo():
    # Retorna como un str el numero del nodo
    global ip_station
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((ip_station, 8000))
    mensaje = 'N-?'
    socket_client.send(mensaje.encode("utf-8"))
    # manejar numero nodo, cuantos hay y ubicacion
    respuesta = socket_client.recv(1024).decode("utf-8")
    socket_client.close()
    if respuesta != 'null':
        respuesta_lt = respuesta.split('_')
        numero_nodo = int(respuesta_lt[0])
        total_nodos = int(respuesta_lt[1])
        coordenadas = respuesta_lt[2].split(',')
        coordenadas = np.array([float(x) for x in coordenadas])
        return numero_nodo, total_nodos, coordenadas
    else:
        return None, None, None
    #return respuesta

def solicitarConexiones(numero_nodo):
    global ip_station
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((ip_station, 8000))
    mensaje = 'N'+str(numero_nodo)+ '-connections'
    socket_client.send(mensaje.encode("utf-8"))
    respuesta = socket_client.recv(1024).decode("utf-8")
    socket_client.close()
    # manejar respuesta
    if respuesta[0] == 'C':
        respuesta = respuesta[2:len(respuesta)]
        vecinos = respuesta.split('-')
        conexiones = []
        betas = []
        for v in vecinos:
            datos = v.split('_')
            conexiones.append(int(datos[0]))
            betas.append(float(datos[1]))
        return conexiones, betas
    else:
        return None, None
    #return respuesta

def solicitarUbicaciones(numero_nodo,  betas, coordenadas_nodo):
    global ip_station
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((ip_station, 8000))
    mensaje = 'N'+str(numero_nodo)+ '-ubications'
    socket_client.send(mensaje.encode("utf-8"))
    respuesta = socket_client.recv(1024).decode("utf-8")
    respuesta = respuesta[2:len(respuesta)]
    # manejar respuesta para obtener ubicaciones
    ubicaciones_str = respuesta.split('_')
    ubicaciones = []
    for i in ubicaciones_str:
        coordenadas = i.split(',')
        coordenadas = [float(x) for x in coordenadas]
        ubicaciones.append(coordenadas)

    mensaje_nueva_ubicacion, nueva_ubicacion = retornarNuevaUbicacion(numero_nodo, ubicaciones, betas, coordenadas_nodo)
    socket_client.send(mensaje_nueva_ubicacion.encode("utf-8"))
    # ejecutar funcion de calcular posicion y devolerla en un mensaje
    # mensaje debe ser de la forma 'N#-x,y,z'
    socket_client.close()
    return nueva_ubicacion

def solicitarInicio(numero_nodo):
    global ip_station
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((ip_station, 8000))
    mensaje = 'N'+str(numero_nodo)+ '-begin'
    socket_client.send(mensaje.encode("utf-8"))
    respuesta = socket_client.recv(1024).decode("utf-8")
    # manejar respuesta
    socket_client.close()
    #retornar bool
    if respuesta == 'SI':
        return True
    else:
        return False


def retornarNuevaUbicacion(numero_nodo, ubicaciones, betas, coordenadas_nodo):
    nuevas_coordenadas = implementacionConsensus.mainConsensus(ubicaciones, betas, coordenadas_nodo)
    mensaje = 'N'+str(numero_nodo)+ '-' + str(nuevas_coordenadas[0])
    for x in range(1, len(nuevas_coordenadas)):
        mensaje = mensaje+ ',' + str(nuevas_coordenadas[x])
    return mensaje, nuevas_coordenadas



