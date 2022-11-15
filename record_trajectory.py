from reachy.trajectory import TrajectoryRecorder, TrajectoryPlayer
from reachy import parts, Reachy
import numpy as np
import time
from serial_utils import get_or_list_available_ports 

from src.rehabot_arm import RehabotArm
from src.usb_io import UsbIO
from src.usb_motor import UsbMotor

#Instanciando o robô
port = get_or_list_available_ports()
io = UsbIO(part_name='right_arm', port=port)
reachy = Reachy(
    right_arm=RehabotArm(io=io),  
)

file_name = input("Insira o nome da gravação: ")
input("Pressione enter para iniciar a gravação!! ")

#Gravar o movimento
print("Iniciando gravação...")

# motors = reachy.right_arm.motors

motors = [
    reachy.right_arm.hand.wrist_pitch,
    reachy.right_arm.hand.wrist_roll,
    reachy.right_arm.hand.forearm_yaw
]

for motor in motors:
    motor.compliant = True


recorder = TrajectoryRecorder(motors, freq = 50)
recorder.start()

input("Pressione enter para parar a gravação!! ")

recorder.stop()
print("Parando gravação...")
print(recorder.trajectories)
np.savez(f'records/{file_name}.npz', **recorder.trajectories)
