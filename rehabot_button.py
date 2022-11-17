from RPi import GPIO
import time
from operator import attrgetter

from reachy.trajectory import TrajectoryRecorder, TrajectoryPlayer
from reachy import parts, Reachy
import numpy as np
import time
from serial_utils import get_or_list_available_ports 

from src.rehabot_arm import RehabotArm
from src.usb_io import UsbIO
from src.usb_motor import UsbMotor

#Instanciando o robô
#Para escolher a porta quando tem mais coisas conectadas
# port = get_or_list_available_ports() 
port = '/dev/ttyUSB0'


#instanciando os botões
LED_RECORDING = 3
LED_PLAYING = 5
LED_READY = 7
BTN_PLAY = 11
BTN_RECORD = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BTN_RECORD, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN_PLAY, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED_READY, GPIO.OUT)
GPIO.setup(LED_RECORDING, GPIO.OUT)
GPIO.setup(LED_PLAYING, GPIO.OUT)

reachy= None

def init_reachy():
    if not reachy:
        io = UsbIO(part_name='right_arm', port=port)
        reachy = Reachy(
            right_arm=RehabotArm(io=io),  
        )


def set_led_recording(on: bool):
    GPIO.output(LED_RECORDING, 0 if on else 1) 

def set_led_ready(on: bool):
    GPIO.output(LED_READY, 0 if on else 1) 

def set_led_playing(on: bool):
    GPIO.output(LED_PLAYING, 0 if on else 1)

def record():
    init_reachy()
    #habilita todos os motores      
    motors = reachy.right_arm.motors 

    #habilita apenas motores especificados
    # motors = [
    #     reachy.right_arm.hand.wrist_pitch,
    #     reachy.right_arm.hand.wrist_roll,
    #     reachy.right_arm.hand.forearm_yaw
    # ]

    for motor in motors:
        motor.compliant = True

    recorder = TrajectoryRecorder(motors, freq = 100)
    recorder.start()

    while True:
        if GPIO.input(BTN_RECORD):
            break
        time.sleep(0.1)

    recorder.stop()
    print("Parando gravação...")
    np.savez(f'records/botao.npz', **recorder.trajectories)


def play():
    init_reachy()
    my_loaded_trajectory = np.load(f'records/botao.npz')

    motors = list([*my_loaded_trajectory.keys()])
    print('Juntas gravadas: ', motors)

    #Habilita torque nos motores que foram gravados
    for motor_name in motors: 
        motor = attrgetter(motor_name)(reachy)
        motor.compliant = False
        motor._motor.p_gain = 8

    trajectory_player = TrajectoryPlayer(reachy, my_loaded_trajectory, freq = 100)
    trajectory_player.play(wait=True, fade_in_duration=2)

    #Desabilita torque nos motores que foram gravados
    for motor_name in motors: 
        motor = attrgetter(motor_name)(reachy)
        motor.compliant = True

def main():
    #Pisca todos os leds ao iniciar
    for i in range(10):
        state = i % 2 == 0
        set_led_recording(state)
        set_led_playing(state)
        set_led_ready(state)

    set_led_recording(False)
    set_led_playing(False)
    set_led_ready(True)
    try:
        while True:
            if GPIO.input(BTN_RECORD):
                print("Iniciando gravação...")
                set_led_recording(True)
                set_led_ready(False)
                time.sleep(1)
                record()
                set_led_recording(False)
                set_led_ready(True)
                time.sleep(5)
            elif GPIO.input(BTN_PLAY):
                set_led_playing(True)
                set_led_ready(False)
                print("Iniciando gravação...")
                time.sleep(1)
                play()
                set_led_playing(False)
                set_led_ready(True)
                time.sleep(5)
            time.sleep(0.01)
    except Exception as e:
        print('Error', str(e))
        set_led_recording(False)
        set_led_playing(False)
        set_led_ready(False)
        
if __name__ == "__main__":
    time.sleep(10)
    main()