import paho.mqtt.client as mqtt
import serial
import sys
import os
import math
import time
import signal
from Queue import Queue

lightSensor_old = 0
threshold_old = 0
connected=Queue()

flag = 0
set_light = 1
set_thresh = 1

client = mqtt.Client()

def signal_handler(signal, frame):
	print "Graceful Disconnect"	
	global client
	client.publish("Status/Arduino", payload = "offline", qos = 2, retain = True)	
	time.sleep(1)	
	client.disconnect()
	time.sleep(1)	
	sys.exit(1)

#def on_disconnect(client, userdata, rc):
#	print "Graceful Disconnect"
#	os._exit(0)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("lightSensor", 2)
	client.subscribe("threshold", 2)
	connected.put(1)
	client.publish("Status/Arduino", payload = "online", qos = 2, retain = True)
	
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
        global lightSensor_old
	global threshold_old        
	print "Subscribed topic",(msg.topic+" "+str(msg.payload))
	if msg.topic == "lightSensor":
		#lightvalue_old.put(str(msg.payload))
		lightSensor_old = msg.payload
		#print " LDR old Value: ", lightSensor_old

	elif msg.topic == "threshold":
		#lightthresh_old.put(str(msg.payload))
		threshold_old = msg.payload
		#print "THreshold Old value: ", threshold_old
	else: 
		print "No threshold values updated"

client.on_connect = on_connect
client.on_message = on_message
#client.on_disconnect = on_disconnect

signal.signal(signal.SIGINT, signal_handler)

client.will_set("Status/Arduino", payload = "offline", qos = 2, retain = True)
client.connect("10.139.68.252", 1883, 5)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

client.loop_start()

ser = serial.Serial("/dev/ttyACM0", 9600)
while True:
	#print "Loop"
	s = ser.readline()
	s1 = s.split(":")
	if s1[0] == "LDR":
    		if connected.empty() == 0:		
			#print threshold_old
			lightSensor = s1[1]
			#print "LDR comparison", abs(int(lightSensor)-int(lightSensor_old))
			if abs(int(lightSensor)-int(lightSensor_old)) >= set_light:
				#LDRflag = 1
				lightSensor_old = lightSensor
				client.publish("lightSensor", payload = s1[1], retain = True)
				#print "LDR callback is done"				
				client.publish("threshold", payload = threshold_old, retain = True)
				#print "POT callback is done"
				#print "LDR publishing ", lightSensor,"   ", threshold				
			

	elif s1[0] == "POT":
    		if connected.empty() == 0:
			#print "threshold",s1[1]
			threshold = s1[1]
			#print "POT Comparison", abs(int(threshold)-int(threshold_old))			
			if abs(int(threshold)-int(threshold_old)) >= set_thresh:
				#POTflag = 1
				threshold_old = threshold			
				client.publish("lightSensor", payload = lightSensor_old, retain = True)
				#print "LDR callback is done"
				#print "threshold value published: ", s1[1]
				client.publish("threshold", payload = s1[1], retain = True)
				#print "POT callback is done"
				#print "POT publishing ", lightSensor,"   ", threshold
	
		

	else:
   		print "Error in reading data"


