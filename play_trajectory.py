from reachy.trajectory import TrajectoryRecorder, TrajectoryPlayer
from reachy import parts, Reachy
import numpy as np
import time 
from operator import attrgetter


from src.rehabot_arm import RehabotArm
from src.usb_io import UsbIO
from serial_utils import get_or_list_available_ports

#Instanciando o robô
port = get_or_list_available_ports()
io = UsbIO(part_name='right_arm', port=port)
reachy = Reachy(
    right_arm=RehabotArm(io=io),  
)


file_name = input("Insira o nome da gravação para reproduzir: ")

my_loaded_trajectory = np.load(f'records/{file_name}.npz')

motors = list([*my_loaded_trajectory.keys()])
    
print('Juntas gravadas: ', motors)

input("Pressione enter para iniciar a reprodução!! ")

#Habilita torque nos motores que foram gravados
for motor_name in motors: 
    motor = attrgetter(motor_name)(reachy)
    motor.compliant = False
    motor._motor.p_gain = 8

trajectory_player = TrajectoryPlayer(reachy, my_loaded_trajectory, freq = 200)
trajectory_player.play(wait=True, fade_in_duration=2)

#Desabilita torque nos motores que foram gravados
for motor_name in motors: 
    motor = attrgetter(motor_name)(reachy)
    motor.compliant = True
