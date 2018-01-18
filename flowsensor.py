#!/usr/bin/env python
##############################################################################
#
# Written by Alex Gomez for the Raspberry Pi - 2018
#
# Website:
# Contact: by email
#
# Please feel free to use and modify this code for you own use.
#
# This program is designed to send an email with a subject line,
# an attachment, a sender, multiple receivers, Cc receivers and Bcc receivers.
# In addition it will also read a pre prepared file and use it's contents to
# create the body of the email
# I hope you are enjoy with this example and is usefull for you
#
#
#Python 3 program for flow meter
#'''This is a Python3 Program for flow meter
#input on pin 27, GND and 5vcc pin rpi zero
# NOW resistor and nothing, direct to GPIO 27
#WARNING: No stopped flow warning. Only approximate.'''
################################################################################
#import the libraries

import RPi.GPIO as GPIO
import time, sys
import MySQLdb

FLOW_SENSOR = 27      #Create a PIN number variable

GPIO.setmode(GPIO.BCM)#Set up the GPIO

GPIO.setup(FLOW_SENSOR, GPIO.IN, pull_up_down = GPIO.PUD_UP) #Set up FLowsensor detector

global count
count = 0              #Initialize counter to 0

def countPulse(channel):  # function counter the pulse of the sensor
   global count
   if start_counter == 1:
      count = count+1

      flow = count
      print(flow)

GPIO.add_event_detect(FLOW_SENSOR, GPIO.FALLING, callback=countPulse) 

while True:           #Condition while the counter is > to 1 every 60 seconds check if > 1 and commit in the database. 
    try:
        print("waiting irrigation")
        start_counter = 1
        time.sleep(60)
        start_counter = 0
        flow = (count * 60 * 2.25 / 1000) # Calculate the liters per minute, ths value can change depending of the tipe of pump
        print ("The flow is: %.3f Liter/min" % (flow))
        
        if flow > 1: #to avoid introduce 0 values in the ddbb i have create a condition if the value is > 1 commited if not wait for irrigation

            #Open database connection
            db = MySQLdb.connect("localhost", "datalogger","datalogger","datalogger")
            curs = db.cursor()
            SQL = ('''INSERT INTO `irrigation` (`ttime`,`count`,`flow`) VALUES (NOW(),'%s','%i')'''%(count,flow))
            curs.execute(SQL)
            time.sleep(1)
            db.commit()
            print ("Data committed")
            count = 0
    except KeyboardInterrupt:
        print ('\ncaught keyboard interrupt!, bye')
        GPIO.cleanup()
        sys.exit()
