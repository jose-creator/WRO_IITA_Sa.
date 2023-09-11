import RPi.GPIO as GPIO
import time
import motorw


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


TRIG = 16
ECHO = 20
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)


print ('Waiting a few seconds for the sensor to settle')
time.sleep(2)

def distancia():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
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
    print ('Distance:',distance,'cm')
    GPIO.cleanup()   
    time.sleep(0.7)      
        
    return int(distance)


while True:
    distancia()
    a = distancia()
    if a < 12:
        break
        