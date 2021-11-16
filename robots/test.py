import numpy as np
import sys, time
from communication import *

# Se crea una instacia de un robot.
rob = Robots_com()

# Se conecta al robot
rob.connect_to_robot()
print('Robot conectado')

conectado = True
m = ''
while conectado:
    try:
        
        if str(m).upper() == 'Y':
            rob.close_conection()
            conectado = False
        else:
            # Avanza
            velIzq = 500
            velDer = 500
            spds = np.array([velIzq, velDer]).reshape(2, 1)
            rob.send_motors_commands(spds)
            time.sleep(4)

            # giro 90°
            spds = np.array([0, velDer]).reshape(2, 1)
            rob.send_motors_commands(spds)
            time.sleep(1.45)
        

        # if m != 'Y':
        #     m = input('Desconectar?: [Y/N]')
    except:
        rob.close_conection()
        break

    




