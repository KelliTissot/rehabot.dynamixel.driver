from ..src.usb_dlx_server import UsbDlxServer
from time import sleep
from ..src.usb_motor import UsbMotor

usb = UsbDlxServer(port='/dev/ttyUSB0')
mx_28 = UsbMotor(name="teste", motor_id=23, server=usb)
mx_106 = UsbMotor(name="teste", motor_id=20, server=usb)

mx_28.led  = True
mx_106.led  = True

mx_28.target_rot_position = 1000
mx_106.target_rot_position = 1000
sleep(2)

mx_28.target_rot_position = 3000
mx_106.target_rot_position = 3000
sleep(2)

mx_28.compliant = True
mx_106.compliant = True
mx_28.led = False
mx_106.led= False