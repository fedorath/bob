import RPi.GPIO as GPIO
import time
from Adafruit_PWM_Servo_Driver import PWM
from sgh_PCF8591P import sgh_PCF8591P

GPIO.setwarnings(False)
irFL = 7
irFR = 11
irMID = 15

L1 = 26
L2 = 24
R1 = 19
R2 = 21

GPIO.setmode(GPIO.BOARD)
GPIO.setup(irFR, GPIO.IN) #Right IR sensor module
GPIO.setup(irMID, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Activation button
GPIO.setup(irFL, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left IR sensor module

GPIO.setup(L1,GPIO.OUT) #Left motor control
GPIO.setup(L2,GPIO.OUT) #Left motor control
GPIO.setup(R1,GPIO.OUT) #Right motor control
GPIO.setup(R2,GPIO.OUT) #Right motor control

#Motor stop/brake
GPIO.output(L1,0) 
GPIO.output(L2,0)
GPIO.output(R1,0)
GPIO.output(R2,0)

speed = 40

def goBoth(speed):
    if speed<0:
        reverse(abs(speed))
    else:
        forward(speed)
		
def irLeft():
    if GPIO.input(irFL)==0:
        return True
    else:
        return False
    
# irRight(): Returns state of Right IR Obstacle sensor
def irRight():
    if GPIO.input(irFR)==0:
        return True
    else:
        return False
    
# irCentre(): Returns state of Centre IR Obstacle sensor
# (Not available on Pi2Go-Lite)
def irCentre():
    if PGType != PGFull:
        return False
    if GPIO.input(irMID)==0:
        return True
    else:
        return False

pwm = PWM(0x40, debug = False)
        pwm.setPWMFreq(60)
 #use pwm on inputs so motors don't go too fast
GPIO.setup(26, GPIO.OUT)
p = GPIO.PWM(26, 20)
p.start(0)

GPIO.setup(24, GPIO.OUT)
q = GPIO.PWM(24, 20)
q.start(0)

GPIO.setup(19, GPIO.OUT)
a = GPIO.PWM(19, 20)
a.start(0)

GPIO.setup(21, GPIO.OUT)
b = GPIO.PWM(21, 20)
b.start(0)






flag=0
while True:
	j=GPIO.input(13)
	if j==1: #Robot is activated when button is pressed
		flag=1
		print "Robot Activated",j
	
	while flag==1:
		i=GPIO.input(7) #Listening for output from right IR sensor
		k=GPIO.input(11) #Listening for output from left IR sensor
		if i==0: #Obstacle detected on right IR sensor
			print "Obstacle detected on Right",i 
			#Move in reverse direction
    			p.ChangeDutyCycle(0)
    			q.ChangeDutyCycle(speed)
    			a.ChangeDutyCycle(0)
    			b.ChangeDutyCycle(speed)
    			q.ChangeFrequency(speed + 5)
    			b.ChangeFrequency(speed + 5)

			#Turn robot left
    			p.ChangeDutyCycle(0)
    			q.ChangeDutyCycle(speed)
    			a.ChangeDutyCycle(speed)
    			b.ChangeDutyCycle(0)
    			q.ChangeFrequency(speed + 5)
    			a.ChangeFrequency(speed + 5)
		if k==0: #Obstacle detected on left IR sensor
			print "Obstacle detected on Left",k
    			p.ChangeDutyCycle(0)
    			q.ChangeDutyCycle(speed)
    			a.ChangeDutyCycle(0)
    			b.ChangeDutyCycle(speed)
    			q.ChangeFrequency(speed + 5)
    			b.ChangeFrequency(speed + 5)
			
    			p.ChangeDutyCycle(speed)
    			q.ChangeDutyCycle(0)
    			a.ChangeDutyCycle(0)
    			b.ChangeDutyCycle(speed)
    			p.ChangeFrequency(speed + 5)
    			b.ChangeFrequency(speed + 5)

		elif i==0 and k==0:
			print "Obstacles on both sides"
    			p.ChangeDutyCycle(0)
    			q.ChangeDutyCycle(speed)
    			a.ChangeDutyCycle(0)
    			b.ChangeDutyCycle(speed)
    			q.ChangeFrequency(speed + 5)
    			b.ChangeFrequency(speed + 5)

    			p.ChangeDutyCycle(speed)
    			q.ChangeDutyCycle(0)
    			a.ChangeDutyCycle(0)
    			b.ChangeDutyCycle(speed)
    			p.ChangeFrequency(speed + 5)
    			b.ChangeFrequency(speed + 5)
			
		elif i==1 and k==1:	#No obstacles, robot moves forward
			print "No obstacles",i
			#Robot moves forward
    			p.ChangeDutyCycle(speed)
    			q.ChangeDutyCycle(0)
    			a.ChangeDutyCycle(speed)
    			b.ChangeDutyCycle(0)
   			p.ChangeFrequency(speed + 5)
    			a.ChangeFrequency(speed + 5)
		j=GPIO.input(13)
		if j==1: #De activate robot on pushin the button
			flag=0
			print "Robot De-Activated",j
    			p.ChangeDutyCycle(0)
    			q.ChangeDutyCycle(0)
    			a.ChangeDutyCycle(0)
    			b.ChangeDutyCycle(0)
