
import socket
import numpy as np


# Dado que la estacion es la que recive todad las solicitudes por medio de su socket de servidor
# es necesario que el atacante mande mensajes a la estación con el objetivo de simular el ataque
# Inicialmente se daran dos tipos de ataques
# 1. uno donde se simulara el ataque a un nodo autonomo,y por lo tanto la ubicación de ese nodo estara mal
# para todos aquellos que tengan acceso a esta
# 2. otro donde se ataquen puntualmente conexiones entre nodos, y por lo tanto se ataca la información
# puntual que sale de un nodo y llega a otro


global ip_station

#Asignar el numero de la ip de la estacion
ip_station = 'localhost'


# Dado que se deben mandar mensaje a la estacion para iniciar un ataque se definira un mensaje por cada uno de 
# los posibles ataques 


# Funcion para simular ataque sobre un nodo
# En este caso a la ubicación del nodo se le puede aplicar un factor de error, dado por el atacante
# o se le puede proporcionar una ubicacion fija erronea
# el mensaje se establece como 'ataque-nodo_#_tipo_x;y;z'
def atacarNodo(numero_nodo, posiciones, tipo_ataque):
    # numero_nodo: es un int con el indicador del nodo que se quiere atacar
    # posiciones: es una lista con el factor de error que se le aplicara a cada posicion del agente
    #             o la posicion fija que se le asignara.
    # tipo_ataque: puede ser 'fijo' para establecer un valor predeterminado a la informacion
    #               que envia un agente, o 'factor' para añadir un factor de error a la informacion
    global ip_station
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((ip_station, 8000))
    mensaje = 'ataque-nodo_'+str(numero_nodo)+'_'+ tipo_ataque +'_'+ str(posiciones[0])
    for i in range(1,len(posiciones)):
        mensaje = mensaje + ';' + str(posiciones[i])
    socket_client.send(mensaje.encode("utf-8"))
    # manejar la respuesta de la confirmacion del ataque exitoso
    respuesta = socket_client.recv(1024).decode("utf-8")
    socket_client.close()




# Funcion para atacar la conexion entre dos nodos.

# Para esto el atacante puede obtener la informacion de las conexiones 
# simulando ser un nodo por medio de la siguiente funcion
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
        return conexiones
    else:
        return None

# Con base en la informacion de las conexiones se puede proceder a atacar una conexion especifica
# A esta conexion se le puede atacar dandole un factor de error a la informacion transmitida 
# o estableciendo un mensaje unico predeterminado que va a mandar el agente
# el mensaje sera 'ataque-conexion_tipo_#1_#2_x;y;z'
def atacarConexion(numero_nodo_origen, numero_nodo_destino, tipo_ataque, posiciones):
    # tipo_ataque: puede ser 'fijo' para establecer un valor predeterminado a la informacion
    #               que envia un agente, o 'factor' para añadir un factor de error a la informacion
    # posiciones: dependiendo del tipo de ataque puede ser la ubicacion predeterminada que se le dara al agente
    #             o el factor de error que se adicionara
    global ip_station
    mensaje = 'ataque-conexion_' + tipo_ataque + '_' + str(numero_nodo_origen)+ '_' +str(numero_nodo_destino)+ '_' + str(posiciones[0])
    for i in range(1, len(posiciones)):
        mensaje = mensaje + ';'+ str(posiciones[i])
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((ip_station, 8000))
    socket_client.send(mensaje.encode("utf-8"))
    # manejar respuesta de confirmacion del ataque
    respuesta = socket_client.recv(1024).decode("utf-8")
    socket_client.close()
