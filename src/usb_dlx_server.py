# Adaptador para conexão USB Serial com motores Dynamixel MX

import os
import math
from threading import Semaphore
import logging

logger = logging.getLogger('UsbDlxServer')

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
ADDR_MX_P_GAIN = 28


class UsbDlxServer():
    def __init__(self, port:str, baudrate=1_000_000, protocol_version=1.0):
        self.port = port
        self.baudrate = baudrate
        self.protocol_version = protocol_version
        self.portHandler = PortHandler(port)
        self.open()
        self.semaphore = Semaphore()

    def open(self):
        logger.info(f'Conectando a porta {self.port} em {self.baudrate}')
        if not self.portHandler.openPort():
            raise Exception(f'Falha ao conectar na porta {self.port}')
        if not self.portHandler.setBaudRate(self.baudrate):
            raise Exception(f'Falha ao setar o baudrate em {self.baudrate}')
        
    def close(self):
        self.portHandler.closePort()

    def _write2ByteTxRx(self, motor_id:int, address: int, value: int, retry=5):
        self.semaphore.acquire()
        logger.debug(f'UsbDlxServer gravando 2 bytes ({value})  no motor {motor_id} no endereço {address}')
        packetHandler = PacketHandler(self.protocol_version)
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(self.portHandler, motor_id, address, int(value))
        self.semaphore.release()
        if dxl_comm_result != COMM_SUCCESS:
            logger.error("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            if retry > 0:
                logger.debug(f'Retenando {retry}')
                self._write2ByteTxRx(motor_id, address, value, retry - 1)
            else:
                raise Exception(f"{packetHandler.getTxRxResult(dxl_comm_result)} - ID: {motor_id}")
        elif dxl_error != 0:
            logger.error("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            logger.info(f'Gravado ({value})  no motor {motor_id} no endereço {address}')

    def _write1ByteTxRx(self, motor_id:int, address: int, value: int, retry = 5):
        self.semaphore.acquire()
        logger.info(f'UsbDlxServer gravando 1 byte ({value}) no motor {motor_id} no endereço {address}')
        packetHandler = PacketHandler(self.protocol_version)
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(self.portHandler, motor_id, address, int(value))
        self.semaphore.release()
        if dxl_comm_result != COMM_SUCCESS:
            logger.error("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            if retry > 0:
                logger.debug(f'Retenando {retry}')
                self._write1ByteTxRx(motor_id, address, value, retry - 1)
            else:
                raise Exception(f"{packetHandler.getTxRxResult(dxl_comm_result)} - ID: {motor_id}")
        elif dxl_error != 0:
            logger.error("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            logger.info(f'Gravado ({value})  no motor {motor_id} no endereço {address}')


    def _read2ByteTxRx(self, motor_id: int, address: int, retry = 5):
        self.semaphore.acquire()
        logger.info(f'UsbDlxServer lendo 2 bytes do motor {motor_id} no endereço {address}')
        packetHandler = PacketHandler(self.protocol_version)
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(self.portHandler, motor_id, address)
        self.semaphore.release()
        if dxl_comm_result != COMM_SUCCESS:
            logger.error("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            if retry > 0:
                logger.debug(f'Retenando {retry}')
                self._read2ByteTxRx(motor_id, address, retry-1)
            else:
                raise Exception(f"{packetHandler.getTxRxResult(dxl_comm_result)} - ID: {motor_id}")
        elif dxl_error != 0:
            logger.error("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            logger.info(f'Resultado do motor {motor_id} no endereço {address}: {dxl_present_position}')
        return dxl_present_position

    def _read1ByteTxRx(self, motor_id: int, address: int, retry = 5):
        self.semaphore.acquire()
        logger.info(f'UsbDlxServer lendo 1 byte do motor {motor_id} no endereço {address}')
        packetHandler = PacketHandler(self.protocol_version)
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(self.portHandler, motor_id, address)
        self.semaphore.release()
        if dxl_comm_result != COMM_SUCCESS:
            logger.error("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            if retry > 0:
                logger.debug(f'Retenando {retry}')
                self._read1ByteTxRx(motor_id, address, retry-1)
            else:
                raise Exception(f"{packetHandler.getTxRxResult(dxl_comm_result)} - ID: {motor_id}")
        elif dxl_error != 0:
            logger.error("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            logger.info(f'>>Resultado do motor {motor_id} no endereço {address}: {dxl_present_position}')
        return dxl_present_position



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
        return self._read2ByteTxRx(motor_id, ADDR_MX_PRESENT_POSITION)

    def set_goal_position(self, motor_id:int, goal_position:int):
        self._write2ByteTxRx(motor_id, ADDR_MX_GOAL_POSITION, goal_position)
    
    def read_goal_position(self, motor_id:int):
        return self._read2ByteTxRx(motor_id, ADDR_MX_GOAL_POSITION)

    def read_temperature(self, motor_id: int):
        return self._read1ByteTxRx(motor_id, ADDR_MX_TEMPERATURE)

    def set_p_gain(self, motor_id: int, gain: int):
        self._write1ByteTxRx(motor_id, ADDR_MX_P_GAIN, gain)

    def read_p_gain(self, motor_id: int):
        self._read1ByteTxRx(motor_id, ADDR_MX_P_GAIN)      
    
