import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.IN) #Right IR sensor module
GPIO.setup(15 , GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Centre Front obstacle sensor
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Left IR sensor module

GPIO.setup(26,GPIO.OUT) #Left motor control
GPIO.setup(24,GPIO.OUT) #Left motor control
GPIO.setup(19,GPIO.OUT) #Right motor control
GPIO.setup(21,GPIO.OUT) #Right motor control

#Motor stop/brake
GPIO.output(26,0) 
GPIO.output(24,0)
GPIO.output(19,0)
GPIO.output(21,0)

flag=0
while True:
	j=GPIO.input(15)
	if j==1: #Robot is activated when button is pressed
		flag=1
		print "Robot Activated",j
	
	while flag==1:
		i=GPIO.input(11) #Listening for output from right IR sensor
		k=GPIO.input(7) #Listening for output from left IR sensor
		if i==0: #Obstacle detected on right IR sensor
			print "Obstacle detected on Right",i 
			#Move in reverse direction
			GPIO.output(26,1) #Left motor turns anticlockwise
			GPIO.output(24,0)  
			GPIO.output(19,1) #Right motor turns clockwise
			GPIO.output(21,0)		
			time.sleep(1)

			#Turn robot left
			GPIO.output(26,0) #Left motor turns clockwise
			GPIO.output(24,1)
			GPIO.output(19,1) #Right motor turns clockwise
			GPIO.output(21,0)
			time.sleep(2)
		if k==0: #Obstacle detected on left IR sensor
			print "Obstacle detected on Left",k
			GPIO.output(26,1)
			GPIO.output(24,0)
			GPIO.output(19,1)
			GPIO.output(21,0)		
			time.sleep(1)

			GPIO.output(26,1)
			GPIO.output(24,0)
			GPIO.output(19,0)
			GPIO.output(21,1)
			time.sleep(2)

		elif i==0 and k==0:
			print "Obstacles on both sides"
			GPIO.output(26,1)
			GPIO.output(24,0)
			GPIO.output(19,1)
			GPIO.output(21,0)		
			time.sleep(2)

			GPIO.output(26,1)
			GPIO.output(24,0)
			GPIO.output(19,0)
			GPIO.output(21,1)
			time.sleep(4)
			
		elif i==1 and k==1:	#No obstacles, robot moves forward
			print "No obstacles",i
			#Robot moves forward
			GPIO.output(26,0)
			GPIO.output(24,1)
			GPIO.output(19,0)
			GPIO.output(21,1)
			time.sleep(0.5)
		j=GPIO.input(15)
		if j==1: #De activate robot on pushin the button
			flag=0
			print "Robot De-Activated",j
			GPIO.output(26,0)
			GPIO.output(24,0)
			GPIO.output(19,0)
			GPIO.output(21,0)
			time.sleep(1)
