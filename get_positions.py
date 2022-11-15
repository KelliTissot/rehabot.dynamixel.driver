from reachy import Reachy
from reachy.trajectory import TrajectoryRecorder, TrajectoryPlayer
from src.usb_io import UsbIO
from src.usb_dlx_server import UsbDlxServer
from src.usb_motor import UsbMotor
from reachy.parts.arm import Arm, RightArm
from reachy.io import IO
from collections import OrderedDict

from src.rehabot_arm import RehabotArm, RehabotHand

#ANTES DE EXECUTAR, COLOCAR TODAS AS JUNTAS NA POSIÇÃO INICIAL DO BRAÇO (RETO)
#USAR OS VALORES DA POSIÇÃO ATUAL COMO OFFSET NEGATIVO

def print_all_positions(io: IO):
    for name in  RehabotArm.dxl_motors:
        config = RehabotArm.dxl_motors[name]
        id = config['id']
        motor = io.find_dxl(name, config)
        position = motor.rot_position
        
        print(f'Motor {name} position \t{position}')

    for name in  RehabotHand.dxl_motors:
        config = RehabotHand.dxl_motors[name]
        id = config['id']
        motor = io.find_dxl(name, config)
        position = motor.rot_position
        
        print(f'Motor {name} position \t{position}')


if __name__ == '__main__':         
    print('EXECUTANDO...')  
    io = UsbIO(part_name='right_arm', port='/dev/ttyUSB0')
    print_all_positions(io)