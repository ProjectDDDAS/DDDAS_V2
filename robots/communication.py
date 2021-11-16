import socket
import sys, time
import numpy as np

class Robots_com():
    def __init__(self):
        self._buffer_size = 256
        self._msg_delimiter = '/'
        self._msg_end = 'z'
        self._msg_tail = self._msg_delimiter + self._msg_end + self._msg_delimiter

        self._robot_ip_address = '192.168.0.57'


        # Initialization
        self.init_robot_message()

    def init_robot_message(self):
        id = '80'
        flags_req = '00'
        flags_set = '00'
        motor_left_LSB = '00'
        motor_left_MSB = '00'
        motor_right_LSB = '00'
        motor_right_MSB = '00'
        leds_state = '00'
        leds_rgb = '00'*12
        sound = '00'
        self._robot_message = [id, flags_req, flags_set,
                               motor_left_LSB, motor_left_MSB,
                               motor_right_LSB, motor_right_MSB,
                               leds_state, leds_rgb, sound]

    def set_robot_leds(self, state='on'):
            msg = self._robot_message.copy()
            if state == 'on':
                msg[7] = '07'
            else:
                msg[7] = '00'
            msg = ''.join(msg)
            msg = bytes.fromhex(msg)
            self._robot_sckt.sendall(msg)


    def connect_to_robot(self):
        # Camera socket (as client)
        self._robot_sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._robot_sckt.connect((self._robot_ip_address, 1000))
        self.set_robot_leds(state = 'on') # To check connection
    

    def map_speed(self, value):
        value = np.clip(value, -1000, 1000)
        value = abs(value) if value >= 0 else 65536 + value # 2**16 = 65536 (Two's complement)
        speed = '000' + hex(int(value))[2:]
        speed = speed[::-1]
        speed = speed[:4][::-1]
        return speed[0:2], speed[2:4] # MSB, LSB


    def send_motors_commands(self, speeds):
        # speeds must be an array of shape (2, 1)
        msg = self._robot_message.copy()
        msg[4], msg[3] = self.map_speed(speeds[0, 0])
        msg[6], msg[5] = self.map_speed(speeds[1, 0])
        msg = ''.join(msg)
        msg = bytes.fromhex(msg)
        self._robot_sckt.sendall(msg)
    def close_conection(self):
        self.set_robot_leds(state = 'off')
        time.sleep(0.5)
        self._robot_sckt.close()
