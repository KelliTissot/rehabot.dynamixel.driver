from RPi import GPIO
import time

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

state = True


GPIO.output(LED_READY, 1) 
GPIO.output(LED_RECORDING, 1) 
GPIO.output(LED_PLAYING, 1) 

while True:
    print(f"BTN_RECORD {GPIO.input(BTN_RECORD)} BTN_PLAY {GPIO.input(BTN_PLAY)} ")
    GPIO.output(LED_READY, 0 if state else 1) 
    GPIO.output(LED_RECORDING, 0 if state else 1) 
    GPIO.output(LED_PLAYING, 0 if state else 1) 
    time.sleep(0.5)
    state = not state
    # if GPIO.input(BTN_1):
    #     print("Botão 1 apertado. ")