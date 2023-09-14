import RPi.GPIO as GPIO
import time
#import cv2
import numpy as np


#configuracion de pines GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
"""
cap=cv2.VideoCapture(0)
lower_range=np.array([150,142,7])
upper_range=np.array([179,255,255])
lower_range1=np.array([56,36,26])
upper_range1=np.array([88,255,255])
"""
in1 = 27
in2 = 22
en = 17

servo_pin = 14

trigger_sensor_frontal = 16
echo_sensor_frontal = 20
trigger_sensor_der = 19
echo_sensor_der = 26
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

# Crear un objeto PWM para controlar la velocidad del motor
 # Frecuencia de PWM: 100 Hz

# Iniciar el PWM con un ciclo de trabajo del 0%

def avanzar():  
    GPIO.output(en,GPIO.HIGH)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    pwm2.ChangeDutyCycle(65)
    
def setAngle(angle):
    duty = angle / 18 + 3
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(duty)
    
def distancia(TRIG, ECHO):
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
    #print ('Distance:',distance,'cm')
    #GPIO.cleanup()   
    #time.sleep(0.7)      
    
    return int(distance)

def red(img):
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower_range,upper_range)
    _,mask1=cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
    cnts,_=cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    a = []
    for c in cnts:
        x=600
        if cv2.contourArea(c)>x:
            x,y,w,h=cv2.boundingRect(c)
            a.append(x)
            x1 = int(x+x+w)//2
            y1 = int(y+y+w)//2
            cv2.circle(img,(x1,y1),4,(255,0,255),-1)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.putText(frame,("DETECT"),(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
    #r=len(a)
    #cv2.putText(frame,("Red: " + str(r)),(111,432),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
    #r1 = str(r)
    
    #return int(r1)

def green(img):
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower_range1,upper_range1)
    _,mask1=cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
    cnts,_=cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    b = []
    for c in cnts:
        x=600
        if cv2.contourArea(c)>x:
            x,y,w,h=cv2.boundingRect(c)
            b.append(x)
            x2 = int(x+x+w)//2
            y2 = int(y+y+w)//2
            cv2.circle(img,(x2,y2),4,(255,0,255),-1)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(frame,("DETECT"),(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)
    #g = len(b)
    #cv2.putText(frame,("Green: " + str(g)),(200,432),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
    #g1 = str(g)
    
    #return int(g1)

"""
while True:
    ret,frame=cap.read()
    frame=cv2.resize(frame,(640,480))
    red(frame)
    green(frame)
    #g2 = int(g1)
    #r2 = int(r1)
    cv2.imshow("FRAME",frame)
    if cv2.waitKey(1)&0xFF==27:
        break
    avanzar() 

    if red(frame) > 0:
        avanzar() 
        setAngle(50)
    elif green(frame) > 0:
        avanzar() 
        setAngle(7)
    else:
        avanzar() 
        setAngle(30)

"""
while True:
    
    dist_frontal = distancia(trigger_sensor_frontal , echo_sensor_frontal)
    dist_der = distancia(trigger_sensor_der , echo_sensor_der)
    dist_izq = distancia(trigger_sensor_izq  , echo_sensor_izq)
    print("frontal =",dist_frontal,"der =", dist_der,"izq =", dist_izq)
    avanzar()
   
    if dist_frontal > 70: 
        print("recto")
        setAngle(33)
       
    """ 
    if dist_izq < 20 and dist_izq < dist_der:
            print("Dobla para la derecha")
            setAngle(37)
        
    if dist_der < 20 and dist_der < dist_izq:
            print("Dobla para la izquierda")
    
            setAngle(28)
    """
    while dist_frontal < 70:
        
        if dist_izq < dist_der:
            print("Dobla para la derecha")
            setAngle(45)
            time.sleep(0.7)
        if dist_der < dist_izq:
            print("Dobla para la izquierda")
            setAngle(18)
            time.sleep(0.7)
        break
            

    #time.sleep(0.4)

           
          
           
          
           
        


