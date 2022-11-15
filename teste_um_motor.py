from logger import init_custom_logger
from src.usb_dlx_server import UsbDlxServer
from time import sleep
from src.usb_motor import UsbMotor

usb = UsbDlxServer(port='/dev/ttyUSB0')
motor = UsbMotor(name="teste", motor_id=10, server=usb)
init_custom_logger()


motor.led  = True
motor.compliant = False
motor.target_rot_position = 0
sleep(2)
motor.compliant = True
motor.led = False
