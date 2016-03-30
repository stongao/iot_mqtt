import paho.mqtt.client as mqtt
import serial
import sys
import os
import thread
from Queue import Queue

connected=Queue()
def serial_reading(threadname,):
    ser = serial.Serial("/dev/ttyACM0", 9600)
    while True:
	s = ser.readline()
	s1 = s.split(":")
	if s1[0] == "LDR":
	    if connected.empty() == 0:		
		#print "lightSensor",s1[1]
                client.publish("L2/lightSensor", payload = s1[1], retain = True)

	elif s1[0] == "POT":
	    if connected.empty() == 0:
	        #print "threshold",s1[1]
                client.publish("L2/threshold", payload = s1[1], retain = True)
	else:
	    print "Error in reading data"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("L2/lightSensor", 2)
	client.subscribe("L2/threshold", 2)
	connected.put(1)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
        pass
        #print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
thread.start_new_thread(serial_reading,("ser",))
client.loop_forever()
'''
def checkthreshold():
	
	if msg.topic == "lightSensor":
		lightSensor = msg.payload
	else: 
		print("Not subscribed to topic: lightSensor")
	
	if msg.topic == "threshold":
		threshold == msg.payload
	else:
		print("Not subscribed to topic: threshold")

if LEDthreshold <= LEDthreshold:
		client.publish("L2/lightStatus", payload = "TurnOn", qos = 2)
	else:
		client.publish("L2/lightStatus", payload = "TurnOff", qos = 2)
'''

