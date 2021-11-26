import communication.attackStationCommunication as attackStationCommunication

def main_consola():
    tipo = input('Ingrese el tipo de ataque que quiere realizar. n para atacar el nodo, c para atacar una conexion puntual: ')
    tipo_puntual = input('Ingrese "p" si quiere hacer un ataque donde la posicion quede predefinida o "e" si quiere agregarle un factor de error a la posicion real del agente: ')
    tipo_ataque = {'p':'fijo', 'e':'factor'}
    contestacion = {'p':'Ingrese la ubicacion que quiere predefinir para el agente. En formato "x;y;z": ','e': 'Ingrese el factor de error que quiere adicionar a la posicion real. En formato "x;y;z": '}
    if tipo == 'n':
        numero_nodo = int(input('Ingrese el numero del nodo que quiere atacar: '))
        posiciciones_str = input(contestacion[tipo_puntual])
        posiciones = posiciciones_str.split(';')
        posiciones = [float(p) for p in posiciones]
        attackStationCommunication.atacarNodo(numero_nodo, posiciones, tipo_ataque[tipo_puntual])
    elif tipo == 'c':
        nodo_origen = int(input('Ingrese el nodo origen desde el cual va a atacar la conexion: '))
        ver_conexiones = input('Desea ver las conexiones posibles de este nodo: (s/n): ')
        if ver_conexiones == 's':
            conexiones = attackStationCommunication.solicitarConexiones(nodo_origen)
            print(conexiones)
        nodo_destino = int(input('\nIngrese el nodo destino del que quiere alterar la comunicacion: '))
        posiciciones_str = input(contestacion[tipo_puntual])
        posiciones = posiciciones_str.split(';')
        posiciones = [float(p) for p in posiciones]
        attackStationCommunication.atacarConexion(nodo_origen, nodo_destino, tipo_ataque[tipo_puntual], posiciones)
def main_autonomo():
    tipo_ataque = 'factor'
    nodo_origen = 1
    nodo_destino = 2
    posiciones = [5.0,2.0]
    #attackStationCommunication.atacarNodo(nodo_origen, posiciones, tipo_ataque)
    #attackStationCommunication.atacarConexion(nodo_origen, nodo_destino, tipo_ataque, posiciones)
    #attackStationCommunication.atacarNodo(nodo_origen, posiciones, "fijo")
    #attackStationCommunication.atacarConexion(nodo_origen, nodo_destino, "fijo", posiciones)

def main():
    metodo = input('Ingrese "m" si quiere ingresar los parametros manualmente, o ingrese "a" si quiere usar los que estan predefinidos: ')
    if metodo == 'm':
        main_consola()
    else:
        main_autonomo()

main()