from usb_dlx_server import UsbDlxServer
from utils import deg_to_int, int_to_deg


class UsbMotor(object):
    def __init__(self, name, motor_id, server:UsbDlxServer):
        print(f'Criando o motor {name} no id {motor_id}')
        self.name = name
        self.server = server
        self.motor_id = motor_id

        # """Check the maximum torque allowed (in %) of the motor."""
        # self._motor.power_ratio_limit

    @property
    def temperature(self):
        return 20 # Reachy tenta ler a temperatura em uma Threade causa problemas de conexão, investigar possibilidate de usar um semáforo
        return self.server.read_temperature(self.motor_id)

    @property
    def rot_position(self):
        position = self.server.read_present_position(self.motor_id)
        return int_to_deg(position)

    @property
    def led(self):
        return self.server.read_led(self.motor_id)
    
    @property
    def compliant(self):
        return not self.server.read_torque(self.motor_id)

    @property
    def target_rot_position(self):
        value = self.server.read_goal_position(self.motor_id)
        return int_to_deg(value)

    @compliant.setter
    def compliant(self, value:bool):
        self.server.set_torque(self.motor_id, not value)

    @led.setter
    def led(self, value:bool):
        self.server.set_led(self.motor_id, value)
    
    @target_rot_position.setter
    def target_rot_position(self, value:int):
        self.server.set_goal_position(self.motor_id, deg_to_int(value))

