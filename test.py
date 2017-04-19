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

while True:
    i=GPIO.input(15) #Listening for output from  IR sensor
	
			#Move in reverse direction
			GPIO.output(26,1) #Left motor turns anticlockwise
			GPIO.output(24,0)  
			GPIO.output(19,1) #Right motor turns clockwise
			GPIO.output(21,0)		
			time.sleep(1)

		 #Obstacle detected on left IR sensor
			print "Obstacle detected on Left"
			GPIO.output(26,0)
			GPIO.output(24,1)
			GPIO.output(19,1)
			GPIO.output(21,0)		
			time.sleep(2)

		else:	#No obstacles, robot moves forward
			print "No obstacles"
			#Robot moves forward
			GPIO.output(26,0)
			GPIO.output(24,1)
			GPIO.output(19,0)
			GPIO.output(21,1)
			
	
