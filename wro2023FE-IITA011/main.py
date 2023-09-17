import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

#configuracion de pines GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

cap=cv2.VideoCapture(0)
lower_range=np.array([150,142,7])
upper_range=np.array([179,255,255])
lower_range1=np.array([65,23,30])
upper_range1=np.array([90,255,230])
lower_range2=np.array([125,67,70])
upper_range2=np.array([168,255,160])
lower_range3=np.array([156,86,63])
upper_range3=np.array([179,167,196])


in1 = 27
in2 = 22
en = 17

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

# Crear un objeto PWM para controlar la velocidad del motor
 # Frecuencia de PWM: 100 Hz

# Iniciar el PWM con un ciclo de trabajo del 0%

def avanzar():  
    GPIO.output(en,GPIO.HIGH)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    pwm2.ChangeDutyCycle(75)
    
    ret,frame=cap.read() 
    red(frame)
    green(frame)
    cv2.imshow("FRAME",frame)
    if cv2.waitKey(1)&0xFF==27:
        print("nada")

def setAngle(angle):
    ret,frame=cap.read() 
    red(frame)
    green(frame)
    cv2.imshow("FRAME",frame)
    if cv2.waitKey(1)&0xFF==27:
        print("nada")
    
    duty = angle / 18 + 3
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    #time.sleep(0.1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(duty)
    
    ret,frame=cap.read() 
    red(frame)
    green(frame)
    cv2.imshow("FRAME",frame)
    if cv2.waitKey(1)&0xFF==27:
        print("nada")

def distancia(TRIG, ECHO):
    ret,frame=cap.read() 
    red(frame)
    green(frame)
    cv2.imshow("FRAME",frame)
    if cv2.waitKey(1)&0xFF==27:
        print("nada") 
    
    count = time.time()
    start = time.time()  
    GPIO.output(TRIG, True)
    time.sleep(0.0000001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0 and time.time()-count<0.1:
        start = time.time()
        
    count = time.time()
    end = time.time()
    while GPIO.input(ECHO)==1 and time.time()-count<0.1:
        end = time.time()
    
    pulse_duration = end - start
    distance = pulse_duration * 17165
    distance = round(distance, 1)
    #print ('Distance:',distance,'cm')
    #time.sleep(0.3)
    
    ret,frame=cap.read() 
    red(frame)
    green(frame)
    cv2.imshow("FRAME",frame)
    if cv2.waitKey(1)&0xFF==27:
        print("nada")
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
            #x1 = int(x+x+w)//2
            #y1 = int(y+y+w)//2
            #cv2.circle(img,(x1,y1),4,(255,0,255),-1)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
            #cv2.putText(frame,("DETECT"),(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
    
    r=len(a)
    #cv2.putText(frame,("Red: " + str(r)),(111,432),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
    
    return int(r)
    

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
            #x2 = int(x+x+w)//2
            #y2 = int(y+y+w)//2
            #cv2.circle(img,(x2,y2),4,(255,0,255),-1)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            #cv2.putText(frame,("DETECT"),(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)
   
    g = len(b)
    #cv2.putText(frame,("Green: " + str(g)),(200,432),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
    
    return int(g)
"""
def Azul(img):
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower_range2,upper_range2)
    _,mask1=cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
    cnts,_=cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    a = []
    for c in cnts:
        x=600
        if cv2.contourArea(c)>x:
            x,y,w,h=cv2.boundingRect(c)
            a.append(x)
            #x1 = int(x+x+w)//2
            #y1 = int(y+y+w)//2
            #cv2.circle(img,(x1,y1),4,(255,0,255),-1)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            #cv2.putText(frame,("DETECT"),(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
    
    A =len(a)
    #cv2.putText(frame,("Azul: " + str(A)),(300,432),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
    
    return int(A)

def naranja(img):
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower_range3,upper_range3)
    _,mask1=cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
    cnts,_=cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    a = []
    for c in cnts:
        x=600
        if cv2.contourArea(c)>x:
            x,y,w,h=cv2.boundingRect(c)
            a.append(x)
            #x1 = int(x+x+w)//2
            #y1 = int(y+y+w)//2
            #cv2.circle(img,(x1,y1),4,(255,0,255),-1)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
            #cv2.putText(frame,("DETECT"),(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)
    
    n =len(a)
    #cv2.putText(frame,("naranja: " + str(n)),(400,432),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
    
    return int(n)
"""

x = 0

while True:
            ret,frame=cap.read()
            frame=cv2.resize(frame,(640,480))
            red(frame)
            green(frame)
            cv2.imshow("FRAME",frame)
            if cv2.waitKey(1)&0xFF==27:
                break
            avanzar()
            x += 1
            
            if x == 2:
                
                ret,frame=cap.read() 
                red(frame)
                green(frame)
                cv2.imshow("FRAME",frame)
                if cv2.waitKey(1)&0xFF==27:
                    break
                
                dist_frontal = distancia(trigger_sensor_frontal , echo_sensor_frontal)
                
                ret,frame=cap.read() 
                red(frame)
                green(frame)
                cv2.imshow("FRAME",frame)
                if cv2.waitKey(1)&0xFF==27:
                    break
                
                dist_der = distancia(trigger_sensor_der , echo_sensor_der)
                
                ret,frame=cap.read() 
                red(frame)
                green(frame)
                cv2.imshow("FRAME",frame)
                if cv2.waitKey(1)&0xFF==27:
                    break
                
                dist_izq = distancia(trigger_sensor_izq  , echo_sensor_izq)
                
                ret,frame=cap.read() 
                red(frame)
                green(frame)
                cv2.imshow("FRAME",frame)
                if cv2.waitKey(1)&0xFF==27:
                    break
                
                print("frontal =",dist_frontal,"der =", dist_der,"izq =", dist_izq)
                
                ret,frame=cap.read() 
                red(frame)
                green(frame)
                cv2.imshow("FRAME",frame)
                if cv2.waitKey(1)&0xFF==27:
                    break
                
                x = 0
                
                ret,frame=cap.read() 
                red(frame)
                green(frame)
                cv2.imshow("FRAME",frame)
                if cv2.waitKey(1)&0xFF==27:
                    break
                
                if dist_frontal < 60:
                    
                    ret,frame=cap.read() 
                    red(frame)
                    green(frame)
                    cv2.imshow("FRAME",frame)
                    if cv2.waitKey(1)&0xFF==27:
                        break
                    
                    if dist_izq < dist_der:
                        
                        ret,frame=cap.read() 
                        red(frame)
                        green(frame)
                        cv2.imshow("FRAME",frame)
                        if cv2.waitKey(1)&0xFF==27:
                            break
                        
                        print("Dobla para la derecha")
                        setAngle(50)
                        
                        ret,frame=cap.read() 
                        red(frame)
                        green(frame)
                        cv2.imshow("FRAME",frame)
                        if cv2.waitKey(1)&0xFF==27:
                            break
                        
                        time.sleep(0.5)
                        
                        ret,frame=cap.read() 
                        red(frame)
                        green(frame)
                        cv2.imshow("FRAME",frame)
                        if cv2.waitKey(1)&0xFF==27:
                            break
                        
                    elif dist_der < dist_izq:
                        
                        ret,frame=cap.read() 
                        red(frame)
                        green(frame)
                        cv2.imshow("FRAME",frame)
                        if cv2.waitKey(1)&0xFF==27:
                            break
                        
                        print("Dobla para la izquierda")
                        setAngle(14)
                        
                        ret,frame=cap.read() 
                        red(frame)
                        green(frame)
                        cv2.imshow("FRAME",frame)
                        if cv2.waitKey(1)&0xFF==27:
                            break
                        
                        time.sleep(0.5)
                        
                        ret,frame=cap.read() 
                        red(frame)
                        green(frame)
                        cv2.imshow("FRAME",frame)
                        if cv2.waitKey(1)&0xFF==27:
                            break
                
                if dist_frontal > 60:
                    
                    ret,frame=cap.read() 
                    red(frame)
                    green(frame)
                    cv2.imshow("FRAME",frame)
                    if cv2.waitKey(1)&0xFF==27:
                            break
                    
                    print("recto")
                    setAngle(30)
                    
                    ret,frame=cap.read() 
                    red(frame)
                    green(frame)
                    cv2.imshow("FRAME",frame)
                    if cv2.waitKey(1)&0xFF==27:
                            break
               
                    if dist_izq < 120 and dist_izq < dist_der:
                            ret,frame=cap.read() 
                            red(frame)
                            green(frame)
                            cv2.imshow("FRAME",frame)
                            if cv2.waitKey(1)&0xFF==27:
                                break
                        
                            print("pared derecha")
                            setAngle(39)
                            
                            ret,frame=cap.read() 
                            red(frame)
                            green(frame)
                            cv2.imshow("FRAME",frame)
                            if cv2.waitKey(1)&0xFF==27:
                                break
                            
                    elif dist_der < 120 and dist_der < dist_izq:
                            ret,frame=cap.read() 
                            red(frame)
                            green(frame)
                            cv2.imshow("FRAME",frame)
                            if cv2.waitKey(1)&0xFF==27:
                                break
                            
                            print("pared izquierda")
                            setAngle(25)
                            
                            ret,frame=cap.read() 
                            red(frame)
                            green(frame)
                            cv2.imshow("FRAME",frame)
                            if cv2.waitKey(1)&0xFF==27:
                                break
         
                ret,frame=cap.read() 
                red(frame)
                green(frame)
                cv2.imshow("FRAME",frame)
                if cv2.waitKey(1)&0xFF==27:
                    break
                
                while red(frame) >= 1 or green(frame) >=1:
                    
                    ret,frame=cap.read() 
                    red(frame)
                    green(frame)
                    cv2.imshow("FRAME",frame)
                    if cv2.waitKey(1)&0xFF==27:
                        break
                    
                    if red(frame) >= 1:
                        
                        ret,frame=cap.read() 
                        red(frame)
                        green(frame)
                        cv2.imshow("FRAME",frame)
                        if cv2.waitKey(1)&0xFF==27:
                            break
                        
                        setAngle(23)
                        print("rojo")
                        
                        ret,frame=cap.read() 
                        red(frame)
                        green(frame)
                        cv2.imshow("FRAME",frame)
                        if cv2.waitKey(1)&0xFF==27:
                            break
                        
                    if green(frame) >= 1:
                        
                        ret,frame=cap.read() 
                        red(frame)
                        green(frame)
                        cv2.imshow("FRAME",frame)
                        if cv2.waitKey(1)&0xFF==27:
                            break
                        
                        setAngle(47)
                        print("verde")
                        
                        ret,frame=cap.read() 
                        red(frame)
                        green(frame)
                        cv2.imshow("FRAME",frame)
                        if cv2.waitKey(1)&0xFF==27:
                            break
                        
                    ret,frame=cap.read() 
                    red(frame)
                    green(frame)
                    cv2.imshow("FRAME",frame)
                    if cv2.waitKey(1)&0xFF==27:
                        break

                """ 
                while Azul(frame) >=1 or naranja(frame) >= 1:
                    
                    ret,frame=cap.read()
                    frame=cv2.resize(frame,(640,480))
                    red(frame)
                    green(frame)
                    cv2.imshow("FRAME",frame)
                    if cv2.waitKey(1)&0xFF==27:
                        break
                    
                    if Azul(frame) >=1:
                        time.sleep(1.5)
                        print("Azul")
                        setAngle(14)
                        time.sleep(1)
                        break
                    elif naranja(frame) >=1:
                        time.sleep(1.5)
                        print("naranja")
                        setAngle(50)
                        time.sleep(1)
                        break
                    """  
                ret,frame=cap.read() 
                red(frame)
                green(frame)
                cv2.imshow("FRAME",frame)
                if cv2.waitKey(1)&0xFF==27:
                    break
                        