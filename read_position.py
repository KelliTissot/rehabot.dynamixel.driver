import time
from reachy import Reachy
from reachy.trajectory import TrajectoryRecorder, TrajectoryPlayer
from logger import CustomFormatter
from serial_utils import get_or_list_available_ports
from src.usb_io import UsbIO
from src.usb_dlx_server import UsbDlxServer
from src.usb_motor import UsbMotor
from reachy.parts.arm import Arm, RightArm
from reachy.parts.hand import RightEmptyHand
from reachy.io import IO
import logging
from logger import init_custom_logger

from src.rehabot_arm import RehabotArm


init_custom_logger()

port = get_or_list_available_ports()
#Instanciando o robô
io = UsbIO(part_name='right_arm', port=port)
reachy = Reachy(
    right_arm=RehabotArm(io=io),  
)

def set_all_compliant(state: bool):
    for motor in reachy.right_arm.motors:
        motor.compliant = state


# set_all_compliant(True)

while True:
    print('Posicao:', reachy.right_arm.shoulder_pitch.present_position)
    time.sleep(1)


