import socket 
import matplotlib.pyplot as plt 


# En la comunicacion entre estacion y nodo, la estacion se comportara como servidor.
# La estacion debe saber cual de los 4 tipos de mensaje le llego y como manejar cada uno de ellos 

def empezarComunicacion(total_nodos, conexiones, ubicaciones, betas):
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind(('192.168.0.101', 8000))
    socket_server.listen(10)
    numero_asignado = 0
    historial_ubicaciones = [ubicaciones.copy()]
    #variables para que el sistema sepa si hay un ataque en progreso
    nodo_fijo = False
    nodo_factor = False
    conexion_fijo = False
    conexion_factor = False
    #variables que definen los valores de los errores
    valor_nodo_fijo = {}
    valor_nodo_factor = {}
    valor_conexion_fija = {}
    valor_conexion_factor = {}
    # Almacena los valores equivocados de la posicion para agentes atacados
    ubicaciones_falsas = None
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
            if nodo_factor or nodo_fijo or conexion_fijo or conexion_factor:
                if conexion_fijo or conexion_factor:
                    if nodo_fijo or nodo_factor:
                        ubicacion_alterada = aplicarAtaqueConexion(conexion_fijo, conexion_factor, valor_conexion_fija, valor_conexion_factor,numero_nodo, ubicaciones_falsas)
                    else:
                        ubicacion_alterada = aplicarAtaqueConexion(conexion_fijo, conexion_factor, valor_conexion_fija, valor_conexion_factor,numero_nodo, ubicaciones)
                    ubicacion_alterada = manejoMensaje3(node_conection, ubicacion_alterada,conexiones, numero_nodo, total_nodos )
                    if nodo_fijo or nodo_factor:
                        ubicaciones_falsas[numero_nodo] = ubicacion_alterada[numero_nodo]
                    else:
                        ubicaciones[numero_nodo] = ubicacion_alterada[numero_nodo]
                        historial_ubicaciones.append(ubicaciones.copy())
                else:
                    ubicaciones_falsas = manejoMensaje3(node_conection, ubicaciones_falsas,conexiones, numero_nodo, total_nodos )
        
                if nodo_fijo or nodo_factor:
                    print(ubicaciones_falsas)
                    ub_real = ubicaciones_falsas[numero_nodo].copy()
                    historial_ubicaciones.append(historial_ubicaciones[-1].copy())
                    historial_ubicaciones[-1][numero_nodo] = ub_real
                    ubicaciones_falsas = aplicarAtaqueNodo(nodo_fijo, nodo_factor, valor_nodo_fijo, valor_nodo_factor, numero_nodo, ubicaciones_falsas)
                    historial_ubicaciones_falsas.append(ubicaciones_falsas.copy())
                
            else:
                ubicaciones = manejoMensaje3(node_conection, ubicaciones,conexiones, numero_nodo, total_nodos )
                historial_ubicaciones.append(ubicaciones.copy())
           
        # mensaje 4
        elif 'begin' in mensaje:
            manejoMensaje4(node_conection, numero_asignado, total_nodos)
        # mensaje 5, recivir finalizaciones de nodos
        elif 'finish' in mensaje:
            numero_nodo = int(mensaje[1])
            numero_asignado = manejoMensaje5(node_conection, numero_asignado, numero_nodo)
            if numero_asignado == 0:
                print('Finalizo el proceso')
                break
        # Proceso para cuando se presenta un atacante
        elif 'ataque' in mensaje:
            #manejo del ataque a un nodo
            if 'nodo' in mensaje:
                variables_ataque = mensaje.split('_')
                if 'fijo' == variables_ataque[2]:
                    nodo_fijo = True
                    valor_nodo_fijo = manejoAtaqueNodo(node_conection,variables_ataque, valor_nodo_fijo)
                elif 'factor' == variables_ataque[2]:
                    print('ataque nodo factor')
                    nodo_factor = True
                    valor_nodo_factor = manejoAtaqueNodo(node_conection, variables_ataque, valor_nodo_factor)
                historial_ubicaciones_falsas = historial_ubicaciones.copy()
                ubicaciones_falsas = aplicarAtaqueNodo(nodo_fijo, nodo_factor, valor_nodo_fijo, valor_nodo_factor, int(variables_ataque[1]), ubicaciones.copy())
                historial_ubicaciones_falsas.append(ubicaciones_falsas.copy())
            #manejo del ataque a una conexion
            elif 'conexion' in mensaje:
                variables_ataque = mensaje.split('_')
                if 'fijo' == variables_ataque[1]:
                    conexion_fijo = True
                    valor_conexion_fija = manejarAtaqueConexion(node_conection,variables_ataque, valor_conexion_fija)
                elif 'factor' == variables_ataque[1]:
                    print('Inicio ataque de conexion factor')
                    conexion_factor = True
                    valor_conexion_factor = manejarAtaqueConexion(node_conection, variables_ataque, valor_nodo_factor)

    graficar(historial_ubicaciones)
    mostrarDistancias(historial_ubicaciones)
    
        
        

    

#solicitud de numero de nodo
def manejoMensaje1(node_conection, numero_asignado,total_nodos, ubicaciones):
    if numero_asignado < total_nodos:
        print('Se asigno el nodo '+str(numero_asignado))
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

def manejoMensaje5(node_conection, numero_asignado, numero_nodo):
    numero_asignado -= 1
    print('El nodo '+str(numero_nodo)+ ' finalizo el proceso')
    node_conection.close()
    return numero_asignado



def graficar(historial_ubicaciones):
    ubicacion_inicial = historial_ubicaciones[0]
    print('tamaño del historial')
    print(len(historial_ubicaciones))
    if len(ubicacion_inicial[0]) == 2:
        fig = plt.figure()
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        ax.patches = []
        draws = []
        colors = ['red', 'blue', 'yellow', 'lime', 'purple']
        for i in range(len(ubicacion_inicial)):
            dr = plt.Circle((ubicacion_inicial[i][0],ubicacion_inicial[i][1]), 0.05,color =colors[i])
            texto1 = plt.text(1,1,'')
            texto1.set_position((ubicacion_inicial[i][0],ubicacion_inicial[i][1]))
            texto1.set_text(str(i)+'-0')
            texto1.set_color('black')
            ax.add_patch(dr)
        ubicacion_final = historial_ubicaciones[-1]
        for u in range(1,len(historial_ubicaciones)-1):
            for i in range(len(ubicacion_inicial)):
                dr = plt.Circle((historial_ubicaciones[u][i][0],historial_ubicaciones[u][i][1]), 0.05,color =colors[i])
                ax.add_patch(dr)
        for i in range(len(ubicacion_inicial)):
            dr = plt.Circle((ubicacion_final[i][0],ubicacion_final[i][1]), 0.05,color =colors[i])
            texto1 = plt.text(1,1,'')
            texto1.set_position((ubicacion_final[i][0],ubicacion_final[i][1]))
            texto1.set_text(str(i)+'-f')
            texto1.set_color('black')
            ax.add_patch(dr)
        for n in range(len(ubicacion_final)):
            for n2 in range(n+1, len(ubicacion_final)):
                plt.plot([ubicacion_final[n][0],ubicacion_final[n2][0]],[ubicacion_final[n][1],ubicacion_final[n2][1]])
        ax.set_ylim(-2,6)
        ax.set_xlim(-2,7)
        plt.show()

def mostrarDistancias(historial_ubicaciones):
    ubicacion_final = historial_ubicaciones[-1]
    for n in range(len(ubicacion_final)):
        for n2 in range(n+1, len(ubicacion_final)):
            dis = calcularDistancia(ubicacion_final[n], ubicacion_final[n2])
            print('Distancia entre nodo '+str(n), ' y el nodo '+ str(n2)+ ' es: '+ str(dis))

def calcularDistancia(ub1, ub2 ):
    res = 0
    for i in range(len(ub1)):
        res += (ub1[i]- ub2[i])**2
    res = res**0.5
    return res


#Funcion para manejar un ataque en un nodo
def manejoAtaqueNodo(node_conection, variables_ataque, valor_nodo):
    nodo_atacado = int(variables_ataque[1])
    posiciones = variables_ataque[3].split(';')
    posiciones = [float(p) for p in posiciones]
    valor_nodo[nodo_atacado] = posiciones
    node_conection.close()
    return valor_nodo

# Funcion para manejar ataques sobre una conexion
def manejarAtaqueConexion(node_conection, variables_ataque, valor_conexion):
    nodo_origen = int(variables_ataque[2])
    nodo_destino = int(variables_ataque[3])
    posiciones = variables_ataque[4].split(';')
    posiciones = [float(p) for p in posiciones]
    valor_conexion[(nodo_origen, nodo_destino)] = posiciones
    node_conection.close()
    return valor_conexion

#funcion para modificar informacion en base a ataques en el nodo
def aplicarAtaqueNodo(nodo_fijo, nodo_factor, valor_nodo_fijo, valor_nodo_factor, numero_nodo, ubicaciones ):
    if nodo_fijo == True:
        if numero_nodo in valor_nodo_fijo.keys():
            pos = valor_nodo_fijo[numero_nodo]
            ubicaciones[numero_nodo] = pos.copy()
    if nodo_factor == True:
        if numero_nodo in valor_nodo_factor.keys():
            desfase = valor_nodo_factor[numero_nodo]
            pos = ubicaciones[numero_nodo]
            nueva_pos = []
            for p in range(len(pos)):
                nueva_pos.append(pos[p]+desfase[p])
            ubicaciones[numero_nodo] = nueva_pos
    return ubicaciones

#funcion para modificar informacion en base a ataques en las conxeiones
def aplicarAtaqueConexion(conexion_fijo, conexion_factor, valor_conexion_fija, valor_conexion_factor,numero_nodo, ubicaciones):
    # se retorna una ubicacion parcial fija si al nodo que se le va a mandar la ubicacion, se encuentra entre uno de los nodos destino
    # de alguna de las conexiones alteradas
    identificador = False
    nodos_origen = []
    ubicacion_alterada = ubicaciones.copy()
    if conexion_fijo:
        for con in valor_conexion_fija.keys():
            if con[1] == numero_nodo:
                identificador = True
                nodos_origen.append(con[0])
        if identificador:
            for nodo in nodos_origen:
                ubicacion_alterada[nodo] = valor_conexion_fija[(nodo, numero_nodo)]
    if conexion_factor:
        for con in valor_conexion_factor.keys():
            if con[1] == numero_nodo:
                identificador = True
                nodos_origen.append(con[0])
        if identificador:
            for nodo in nodos_origen:
                for pos in range(len(ubicacion_alterada[nodo])):
                    ubicacion_alterada[nodo][pos] =ubicacion_alterada[nodo][pos]+ valor_conexion_factor[(nodo, numero_nodo)][pos]
    return ubicacion_alterada

        
