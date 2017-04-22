#!/usr/bin/python

#import the SimpleCV, shutil and the custom  py_gmailer  libraries
from SimpleCV import *
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def gmail(png_file):
	#add your gmail address and get your stored gmail password from keyring
	gmail_acct = "kurtax.h1@googlemail.com"
	#if you are not using keyring, comment out the text below
	#if you are not using keyring, uncomment the text below
	app_spec_pwd = "kurtax%1"

	#create variables for the "to" and "from" email addresses
	TO = ["kurtax.h1@googlemail.com"]
	FROM = "kurtax.h1@googlemail.com"

	#asemble the message as "MIMEMultipart" mixed
	msg = MIMEMultipart('mixed')
	msg['Subject'] = 'Important Message!'
	msg['From'] = FROM
	msg['To'] = ', '.join(TO)
	body = MIMEText('Intruder has been located!', 'plain')
	msg.attach(body)

	#open up an image file and attach it to the message
	img_data = open(png_file, 'rb')
	image = MIMEImage(img_data.read())
	img_data.close()
	msg.attach(image)

	#open up the SMTP server, start a tls connection, login, send, and close
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo
	server.login(gmail_acct, app_spec_pwd)
	server.sendmail(FROM, TO, msg.as_string())
	server.close()

#initialize the camer
cam = Camera()
#set the max display size
display = Display((800,600))

#create a threshold variable to change  motion sensitivity
threshold = 5.0

#set timer variables for email loop
start_time = time.time()
wait_time = 60 #in seconds

#set a streaming variable to stream webcam online
streaming = JpegStreamer("0.0.0.0:1212")

#create destination & backup directories for the pictures
dst = "pic" #destination directory for images
bkp = "pic_bkp" #backup  directory for images

#if the picture directories don't exist, create them
if not os.path.exists("pic"):
	os.makedirs("pic")
if not os.path.exists("pic_bkp"):
	os.makedirs("pic_bkp")

#create a loop that constantly grabs new images from the webcam
while True:
        #set a time variable that updates with the loop
        current_time = time.time()
        #grab an image still from the camera and convert it to grayscale
        img01 = cam.getImage().toGray()
        #wait half a second
        time.sleep(0.5)
	#grab an unedited still to use as our original image
	original = cam.getImage()
        #grab another image still from the camera and conver it to grayscale
        img02 = cam.getImage().toGray()
        #subract the images from each other, binarize and inver the colors
        diff = (img01 - img02).binarize(50).invert()

        #dump all the values into a Numpy matrix and extract the mean avg
        matrix = diff.getNumpy()
        mean = matrix.mean()

	#find and highlight the objects within the image
	blobs = diff.findBlobs()

        #check to see if the wait time has been passed
	if current_time >= (start_time + wait_time):
		#if it has, reset the start time
		start_time = time.time()
		#scan the picture directory for files
		for root, dirs, files in os.walk(dst):
			dst_root = root.replace(dst, bkp)
			#if a file is found in the picture directory, send it to email
			if files:
				firstfile = sorted(files)[0]
				img_mailer = os.path.join(root, firstfile)
				gmail.gmail(img_mailer)
			#move any files in the pic directory to the backup directory
			for file_ in files:
				src_file = os.path.join(root, file_)
				dst_file = os.path.join(dst_root, file_)
				shutil.move(src_file, dst_root)

        #if the mean is greater than our threshold variable, then look for objects
	if mean >= threshold:

		#check to see if any objects were detected
		if blobs:
			#find the central point of each object
			#and draw a red circle around it
			for b in blobs:
				try:
					loc = (b.x,b.y) #locates center of object
					original.drawCircle(loc,b.radius(),Color.GREEN,2)
				except:
					e = sys.exc_info()[0]
		#use the current date to create a unique file name
		timestr = time.strftime("%Y%m%d-%H%M%S")
		
		#initialize the counter variable
		i = 1
		
		#check to see if the filename already exists
		while os.path.exists("pic/motion%s-%s.png" % (timestr, i)):
			#if it does, add one to the filename and try again
			i += 1
		#once a unique filename has been found, save the image
		original.save("pic/motion%s-%s.png" % (timestr, i))
		#print results to terminal
		print("Motion Detected")

	
