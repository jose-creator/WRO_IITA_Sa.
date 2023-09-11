import RPi.GPIO as GPIO
import time
from servo import setAngle
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
servo_pin = 10
# Definir los pines de control del L298N
motor_in1 = 17  # Conectado al pin IN1 del L298N
motor_in2 = 27  # Conectado al pin IN2 del L298N
motor_enable = 22  # Conectado al pin ENABLE del L298N

# Configurar los pines como salidas
GPIO.setup(motor_in1, GPIO.OUT)
GPIO.setup(motor_in2, GPIO.OUT)
GPIO.setup(motor_enable, GPIO.OUT)

# Crear un objeto PWM para controlar la velocidad del motor
motor_pwm = GPIO.PWM(motor_enable, 100)  # Frecuencia de PWM: 100 Hz

GPIO.setup(servo_pin, GPIO.OUT)
pwm= GPIO.PWM(servo_pin, 50)
pwm.start(0)
# Iniciar el PWM con un ciclo de trabajo del 0%
motor_pwm.start(0)

# Función para avanzar
def avanzar():
    GPIO.output(motor_in1, GPIO.LOW)
    GPIO.output(motor_in2, GPIO.HIGH)

# Función para retroceder
def retroceder():
    GPIO.output(motor_in1, GPIO.HIGH)
    GPIO.output(motor_in2, GPIO.LOW)

# Función para detener
def detener():
    GPIO.output(motor_in1, GPIO.LOW)
    GPIO.output(motor_in2, GPIO.LOW)
 
try:
        avanzar()
        motor_pwm.ChangeDutyCycle(100)  
        time.sleep(10)  
        setAngle(48)
        avanzar()
        motor_pwm.ChangeDutyCycle(100)
        setAngle(5)# Cambiar la velocidad del motor (de 0 a 100)
        time.sleep(2)  # Retroceder durante 2 segundos

except KeyboardInterrupt:
    detener()
    motor_pwm.stop()
    GPIO.cleanup()