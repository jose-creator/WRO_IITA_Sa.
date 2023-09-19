import RPi.GPIO as GPIO
import time
from mpu6050 import mpu6050
import math
import numpy as np
#configuracion de pines GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

address = 0x68
sensor = mpu6050(address)
yaw = 0.0
gyro_sacale = math.pi / 180.0
gyro_offset_z = 0.0

sample_rate = 100
sample_interval = 1.0 / sample_rate

in1 = 5
in2 = 6
en = 0

servo_pin = 14

trigger_sensor_frontal = 19
echo_sensor_frontal = 26
trigger_sensor_der = 16
echo_sensor_der = 20
trigger_sensor_izq = 15
echo_sensor_izq = 18


#Configuracion de pines como entradas y salidas
GPIO.setup(trigger_sensor_frontal,GPIO.OUT)
GPIO.setup(echo_sensor_frontal,GPIO.IN)
GPIO.setup(trigger_sensor_der,GPIO.OUT)
GPIO.setup(echo_sensor_der,GPIO.IN)
GPIO.setup(trigger_sensor_izq,GPIO.OUT)
GPIO.setup(echo_sensor_izq,GPIO.IN)


GPIO.setup(servo_pin, GPIO.OUT)

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)

pwm2= GPIO.PWM(en, 50)
pwm2.start(0)  
pwm= GPIO.PWM(servo_pin, 50)
pwm.start(0)

def avanzar(x):  
    GPIO.output(en,GPIO.HIGH)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    pwm2.ChangeDutyCycle(x)

def setAngle(angle):
    duty = angle / 18 + 3
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(duty)

def distancia(TRIG, ECHO):
    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
         global start
         start = time.time()
    
    while GPIO.input(ECHO)==1:
         global end
         end = time.time()

    pulse_duration = end - start
    distance = pulse_duration * 17165
    distance = round(distance, 1)
    time.sleep(0.15)
    #print ('Distance:',distance,'cm')      
    
    return int(distance)

while True:
        start_time = time.time()
        gyro_data = sensor.get_gyro_data()
        gyro_z = (gyro_data['z'] - gyro_offset_z) * gyro_sacale
        yaw += gyro_z * sample_interval
        angular_velocity_z = gyro_data['z']
        #time.sleep(0.5)
        #print(f'Angulo de Giro (Z):{math.degrees(yaw):.2f} grados')

        dist_frontal = distancia(trigger_sensor_frontal , echo_sensor_frontal)
        dist_der = distancia(trigger_sensor_der , echo_sensor_der)
        dist_izq = distancia(trigger_sensor_izq  , echo_sensor_izq)
        print("frontal =",dist_frontal,"der =", dist_der,"izq =", dist_izq)

        avanzar(45)
        if abs(angular_velocity_z) > 100:
            print("recto")
            pwm.ChangeDutyCycle(4.8)
            #time.sleep(0.2)
            
            pwm.ChangeDutyCycle(0)

        if dist_frontal < 60:
            if dist_izq < dist_der:
                    print("Dobla para la derecha")
                    setAngle(50)
                    #time.sleep(0.01)
            elif dist_der < dist_izq:
                    print("Dobla para la izquierda")
                    setAngle(14)
                    #time.sleep(0.01)
         
        else:
            if dist_izq < 65 and dist_izq < dist_der:
                    print("pared derecha")
                    setAngle(35)
                                
            elif dist_der < 65 and dist_der < dist_izq:
                    print("pared izquierda")
                    setAngle(25)

