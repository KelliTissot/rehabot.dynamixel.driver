# REHABOT - Driver USB serial para motores Dynamixel - MX

* Pode ser utilizado para substituir a placa Luos para as bibliotecas Reachy

## Utilização

```bash
#Instalando dependências
python3 -m pip install -r requirements.txt
```

## Exemplo 1 - Comando manual

```python
from .src.usb_dlx_server import UsbDlxServer
from .src.usb_motor import UsbMotor

# Cria conexão com adaptador USB-Serial
usb = UsbDlxServer(port='/dev/ttyUSB0')

# Cria instância do motor
motor = UsbMotor(name="teste", motor_id=23, server=usb)

# Habilita o torque
motor.compliant = False

# Liga led do motor
motor.led  = True

# Le a posição atual
print('Posição atual', motor.rot_position)

# Vai atá a posição 1000
motor.target_rot_position = 1000

# Desabilita o torque
motor.compliant = True

# Desliga o led
motor.led = False

```

## Exemplo 2 - Integração Reachy

```python
from reachy import Reachy, parts
from usb_io import UsbIO


print('Criando Reachy...')
io=UsbIO('left_arm', port='/dev/ttyUSB0')
reachy = Reachy(parts.LeftArm(io=io))


# Le posição atual
print("Present- elbow_pitch", reachy.left_arm.elbow_pitch.present_position)
print("Present- shoulder_pitch", reachy.left_arm.shoulder_pitch.present_position)

# Ativa o torque dos motores
reachy.left_arm.elbow_pitch.compliant = False
reachy.left_arm.shoulder_pitch.compliant = False

# Envia as juntas para as posições desejadas
reachy.goto({
    'left_arm.elbow_pitch': 90,
    'left_arm.shoulder_pitch': 90
}, duration=2, wait=True)

# Le posição atual
print("Present- elbow_pitch", reachy.left_arm.elbow_pitch.present_position)
print("Present- shoulder_pitch", reachy.left_arm.shoulder_pitch.present_position)

# Ativa o torque dos motores
reachy.left_arm.elbow_pitch.compliant = True
reachy.left_arm.shoulder_pitch.compliant = True

```
