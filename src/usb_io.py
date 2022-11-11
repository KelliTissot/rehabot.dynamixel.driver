# IO para substituir driver Luos na integração com biblioteca Reachy

from reachy.io.io import IO
from usb_motor import UsbMotor
from usb_dlx_server import UsbDlxServer

class UsbIO(IO):
    """USB Serial IO implementation."""


    def __init__(self, part_name, port:str):
        """Init an io attached to the given part."""
        print("Criando UsbIO")
        self.part_name = part_name
        self.motors = []
        self.server = UsbDlxServer(port)
  
    def find_dxl(self, dxl_name, dxl_config):
        """Get a specific dynamixel motor from the IO.
        Only goal position is used atm.
        """
        print( 'DLX CONFIGU', dxl_config)
        pos = dxl_config['offset'] * (-1 if dxl_config['orientation'] == 'indirect' else 1)
        m = UsbMotor(name=f'{self.part_name}.{dxl_name}', motor_id=dxl_config['id'], server= self.server)
        self.motors.append(m)
        return m

    def find_fan(self, fan_name):
        """Get a specific fan from its name."""
        return FakeFan()

    def close(self):
        """Close the WS."""
        print('Close...')
        self.server.close()


class FakeFan(object):
    """Fake fan module for API consistensy."""
    def __init__(self):
        print('Criando fan')

    def on(self):
        """Do nothing."""
        pass

    def off(self):
        """Do nothing."""
        pass
