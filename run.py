#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importing all SimpleCV

from SimpleCV import *

import os
# import shutil
import pathlib
import shutil
# Import smtplib, for the sending function

import smtplib



from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

IMG = Camera()

# set the max display size

display = Display((800, 600))

# create a threshold variable to change  motion sensitivity

threshold = 5.0

# set timer variables for email loop

start_time = time.time()
wait_time = 60  # in seconds

# create destination & backup directories for the pictures
Path = "CCTV" #destination directory for images
BPath = "random" #backup  directory for images

if not os.path.exists("CCTV"):
        os.makedirs("CCTV")
        
if not os.path.exists("random"):
        os.makedirs("random")

# create a loop that constantly grabs new images from the webcam

while True:

        # set a time variable that updates with the loop

        current_time = time.time()

        # grab an image still from the camera and convert it to grayscale

        Photo1 = IMG.getImage().toGray()

        # wait half a second

        time.sleep(0.5)

    # grab an unedited still to use as our original image

        Photo = IMG.getImage()

        # grab another image still from the camera and conver it to grayscale

        Photo2 = IMG.getImage().toGray()

        # subract the images from each other, binarize and inver the colors

        diff = (Photo1 - Photo2).binarize(50).invert()

        # dump all the values into a Numpy matrix and extract the mean avg

        matrix = diff.getNumpy()
        mean = matrix.mean()

    # find and highlight the objects within the image

        blobs = diff.findBlobs()

        # check to see if the wait time has been passed

	if current_time >= (start_time + wait_time):
		#if it has, reset the start time
		start_time = time.time()
		#scan the picture directory for files
		for root, dirs, files in os.walk(Path):
			Path_root = root.replace(Path, BPath)
			#if a file is found in the picture directory, send it to email
			if files:
				firstfile = sorted(files)[0]
				img_mailer = os.path.join(root, firstfile)
				gmail(img_mailer)
			#move any files in the pic directory to the backup directory
			for file_ in files:
				src_file = os.path.join(root, file_)
				Path_file = os.path.join(Path_root, file_)
				shutil.move(src_file, Path_root)

        # if the mean is greater than our threshold variable, then look for objects

        if mean >= threshold:

		#check to see if any objects were detected
		if blobs:
			#find the central point of each object
			#and draw a red circle around it
			for b in blobs:
				try:
					loc = (b.x,b.y) #locates center of object
					original.drawCircle(loc,b.radius(),Color.RED,2)
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
		Photo.save("pic/motion%s-%s.png" % (timestr, i))
		#print results to terminal
		print("Motion Detected")

def gmail(png_file):

        msg = MIMEMultipart('mixed')
        msg['Subject'] = 'Important Message!'
        msg['From'] = 'kurtax.h1@googlemail.com'
        msg['Reply-to'] = ', '.join('kurtax.h1@googlemail.com')
        body = MIMEText('Intruder has been located!', 'plain')
        msg.attach(body)

    # open up an image file and attach it to the message

        img_data = open(png_file, 'rb')
        image = MIMEImage(img_data.read())
        img_data.close()
        msg.attach(image)

    # open up the SMTP server, start a tls connection, login, send, and close

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo
        server.login('kurtax.h1@googlemail.com', 'kurtax%1')
        server.sendmail('kurtax.h1@googlemail.com','kurtax.h1@googlemail.com', msg.as_string())
        server.close()
