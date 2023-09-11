import RPi.GPIO as GPIO
from time import sleep

## add your servo BOARD PIN number ##
servo_pin = 8

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setwarnings(False)

pwm= GPIO.PWM(servo_pin, 50)
pwm.start(0)

## edit these duty cycle % values ##
left = 2.5
neutral = 7.5
right = 12
#### that's all folks ####

def setAngle(angle):
    duty = angle / 18 + 3
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(duty)



setAngle(5)
sleep(1)
setAngle(30)
sleep(1)

GPIO.cleanup()