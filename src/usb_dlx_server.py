# Adaptador para conexão USB Serial com motores Dynamixel MX

import os
import math

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *

# Control table address
 # Control table address is different in Dynamixel model
ADDR_MX_TORQUE_ENABLE      = 24              
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36
ADDR_MX_LED = 25
ADDR_MX_TEMPERATURE = 43


class UsbDlxServer():
    def __init__(self, port:str, baudrate=1_000_000, protocol_version=1.0):
        self.port = port
        self.baudrate = baudrate
        self.portHandler = PortHandler(port)
        self.packetHandler = PacketHandler(protocol_version)
        self.open()

    def open(self):
        print(f'Conectando a porta {self.port} em {self.baudrate}')
        if not self.portHandler.openPort():
            raise Exception(f'Falha ao conectar na porta {self.port}')
        if not self.portHandler.setBaudRate(self.baudrate):
            raise Exception(f'Falha ao setar o baudrate em {self.baudrate}')
        
    def close(self):
        self.portHandler.closePort()

    def _write4ByteTxRx(self, motor_id:int, address: int, value: int):
        print(f'>>UsbDlxServer gravando 4 bytes ({value})  no motor {motor_id} no endereço {address}')
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, motor_id, address, int(value))
        if dxl_comm_result != COMM_SUCCESS:
            pass
            # print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        print('>>Gravado')

    def _write1ByteTxRx(self, motor_id:int, address: int, value: int):
        print(f'>>UsbDlxServer gravando 1 byte ({value}) no motor {motor_id} no endereço {address}')
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, motor_id, address, int(value))
        if dxl_comm_result != COMM_SUCCESS:
            pass
            # print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        print('>>Gravado')

    def _read4ByteTxRx(self, motor_id: int, address: int):
        # print(f'>>UsbDlxServer lendo 4 bytes do motor {motor_id} no endereço {address}')
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, motor_id, address)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        # print('>>Resultado:', dxl_present_position)
        return dxl_present_position

    def _read1ByteTxRx(self, motor_id: int, address: int):
        # print(f'>>UsbDlxServer lendo 1 byte do motor {motor_id} no endereço {address}')
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, motor_id, address)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        return dxl_present_position
        # print('>>Resultado:', dxl_present_position)


    def set_led(self, motor_id:int,  state:bool):
        value = 1 if state else 0
        self._write1ByteTxRx(motor_id, ADDR_MX_LED, value)

    def read_led(self, motor_id: int):
        return self._read1ByteTxRx(motor_id, ADDR_MX_LED)

    def set_torque(self, motor_id:int, enable:bool):
        value = 1 if enable else 0
        self._write1ByteTxRx(motor_id, ADDR_MX_TORQUE_ENABLE, value)
    
    def read_torque(self, motor_id:int):
        enabled = self._read1ByteTxRx(motor_id, ADDR_MX_TORQUE_ENABLE)
        return True if enabled else False

    def read_present_position(self, motor_id: int):
        return self._read4ByteTxRx(motor_id, ADDR_MX_PRESENT_POSITION)

    def set_goal_position(self, motor_id:int, goal_position:int):
        self._write4ByteTxRx(motor_id, ADDR_MX_GOAL_POSITION, goal_position)
    
    def read_goal_position(self, motor_id:int):
        return self._read4ByteTxRx(motor_id, ADDR_MX_GOAL_POSITION)

    def read_temperature(self, motor_id: int):
        return self._read1ByteTxRx(motor_id, ADDR_MX_TEMPERATURE)
    
