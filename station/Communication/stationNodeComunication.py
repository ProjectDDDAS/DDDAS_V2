import socket 


# En la comunicacion entre estacion y nodo, la estacion se comportara como servidor.
# La estacion debe saber cual de los 4 tipos de mensaje le llego y como manejar cada uno de ellos 

def empezarComunicacion(total_nodos, conexiones, ubicaciones, betas):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind(('192.168.0.101', 8000))
    socket_server.listen(10)
    numero_asignado = 0
    while True:
        node_conection, node_addr = socket_server.accept()
        mensaje = node_conection.recv(1024).decode("utf-8")
        # definir tratamiento tipo de mensajes
        # mensaje 1
        # El mensaje se envia como '#_@_x,y,z' donde # es el numero del nodo,@ es el numero de nodos del sistema y x,y,z 
        # son las coordenadas iniciales del agente
        if mensaje[-1] =='?':
            numero_asignado = manejoMensaje1(node_conection, numero_asignado, total_nodos, ubicaciones)
        # mensaje 2
        # El mensaje se envia como "C-#_%-#_%" donde # es el numero del nodo al cual tiene conexion y % es la distancia deseada
        elif 'connections' in mensaje:
            numero_nodo = int(mensaje[1])
            manejoMensaje2(node_conection,conexiones, numero_nodo, total_nodos, betas)
        # mensaje 3
        # El mensaje se envia como 'U_x,y,z_x1,y1,z1' donde x,y,z es la ubicacion de los nodos que tienen conexion
        # estan en el mismo orden en el que se enviaron los numeros de los nodos (de menor a mayor)
        elif 'ubications' in mensaje:
            numero_nodo = int(mensaje[1])
            ubicaciones = manejoMensaje3(node_conection, ubicaciones,conexiones, numero_nodo, total_nodos )
        # mensaje 4
        elif 'begin' in mensaje:
            manejoMensaje4(node_conection, numero_asignado, total_nodos)

#solicitud de numero de nodo
def manejoMensaje1(node_conection, numero_asignado,total_nodos, ubicaciones):
    if numero_asignado < total_nodos:
        mensaje = str(numero_asignado)+'_'+str(total_nodos)
        coordenadas = ubicaciones[numero_asignado]
        mensaje = mensaje + '_'+ str(coordenadas[0])
        for i in range(1,len(coordenadas)):
            mensaje = mensaje + ',' + str(coordenadas[i])
        node_conection.send(mensaje.encode("utf-8"))
        node_conection.close()
        return numero_asignado+1
    else:
        mensaje = 'null'
        node_conection.send(mensaje.encode("utf-8"))
        print('Se conecto un nodo mas de los que se definieron')
        node_conection.close()
        return numero_asignado

# solicitud de conecciones
def manejoMensaje2(node_conection, conexiones, numero_nodo, total_nodos , betas):
    # se asume que conexiones es una matriz que define que nodos se conectan, 
    # la fila es el nodo del que se quiere saber las conexiones, y hay uno en las 
    # conexiones y 0 en las que no.
    mensaje = 'C'
    for i in range(total_nodos):
        if conexiones[numero_nodo][i] == 1:
            mensaje = mensaje +'-'+ str(i) + '_' + str(betas[numero_nodo][i])
    node_conection.send(mensaje.encode("utf-8"))
    node_conection.close()

# solicitud ubicaciones
def manejoMensaje3(node_conection, ubicaciones, conexiones, numero_nodo, total_nodos):
    # se asume que ubicaciones es una lista con las ubicaciones de los nodos, cada ubicacion es una lista, y cada x es un float
    mensaje = 'U'
    for i in range(total_nodos):
        if conexiones[numero_nodo][i] == 1:
            mensaje = mensaje + '_'
            ubicacion = ubicaciones[i]
            mensaje = mensaje + str(ubicacion[0])
            for j in range(1,len(ubicacion)):
                mensaje = mensaje + ','+ str(ubicacion[j])
    node_conection.send(mensaje.encode("utf-8"))
    # se debe recivir el mensaje con la nueva ubicacion del nodo
    # esta info esta de la forma 'N#-x,y,z

    # depronto toque hacer un ciclo o esperar respuesta
    
    nueva_ubicacion = node_conection.recv(1024).decode("utf-8")
    if nueva_ubicacion[1] == str(numero_nodo):
        nueva_ubicacion = nueva_ubicacion[3:len(nueva_ubicacion)]
        coordenadas = []
        for x in nueva_ubicacion.split(','):
            coordenadas.append(float(x))
        ubicaciones[numero_nodo] = coordenadas
    
    node_conection.close()
    return ubicaciones


def manejoMensaje4(node_conection, numero_asignado, total_nodos):
    if numero_asignado == total_nodos:
        mensaje = 'SI'
    else:
        mensaje = 'NO'
    node_conection.send(mensaje.encode("utf-8"))
    node_conection.close()
