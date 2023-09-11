import RPi.GPIO as GPIO
import time

# Configurar los pines de la Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Definir los pines de control del L298N
motor_in1 = 27  # Conectado al pin IN1 del L298N
motor_in2 = 22  # Conectado al pin IN2 del L298N
motor_enable = 17  # Conectado al pin ENABLE del L298N

# Configurar los pines como salidas
GPIO.setup(motor_in1, GPIO.OUT)
GPIO.setup(motor_in2, GPIO.OUT)
GPIO.setup(motor_enable, GPIO.OUT)

# Crear un objeto PWM para controlar la velocidad del motor
motor_pwm = GPIO.PWM(motor_enable, 100)  # Frecuencia de PWM: 100 Hz

# Iniciar el PWM con un ciclo de trabajo del 0%
motor_pwm.start(0)

# Función para avanzar
def avanzar():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_in1, GPIO.OUT)
    GPIO.setup(motor_in2, GPIO.OUT)
    GPIO.setup(motor_enable, GPIO.OUT)
    GPIO.output(motor_in1, GPIO.HIGH)
    GPIO.output(motor_in2, GPIO.LOW)
    GPIO.output(motor_enable, GPIO.HIGH)

# Función para retroceder
def retroceder():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_in1, GPIO.OUT)
    GPIO.setup(motor_in2, GPIO.OUT)
    GPIO.setup(motor_enable, GPIO.OUT)
    GPIO.output(motor_in1, GPIO.LOW)
    GPIO.output(motor_in2, GPIO.HIGH)

# Función para detener
def detener():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_in1, GPIO.OUT)
    GPIO.setup(motor_in2, GPIO.OUT)
    GPIO.setup(motor_enable, GPIO.OUT)
    GPIO.output(motor_in1, GPIO.LOW)
    GPIO.output(motor_in2, GPIO.LOW)

try:
    while True:
        avanzar()
        motor_pwm.ChangeDutyCycle(50)  # Cambiar la velocidad del motor (de 0 a 100)
        time.sleep(2)  # Avanzar durante 2 segundos

        retroceder()
        motor_pwm.ChangeDutyCycle(50)  # Cambiar la velocidad del motor (de 0 a 100)
        time.sleep(2)  # Retroceder durante 2 segundos

except KeyboardInterrupt:
    detener()
    motor_pwm.stop()
    GPIO.cleanup()
