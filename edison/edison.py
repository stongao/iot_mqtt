# File: edison.py
# Team: Group8
# Description: This file will run on the intel edison
#   The edison connects to the broker at IP address 'brokerIP'at port brokerPort
#   and subscribes to lightStatus, Status/Arduino, Status/RaspPi
#   depending on recieved values it will Turn On/Off respective LEDs


import paho.mqtt.client as mqtt
import sys
import mraa


brokerIP = '10.139.68.252' #mqtt broker IP address (PC1)
brokerPort = 1883 #mqtt broker Port number 
keepAlive = 60 #keep alive timer


# initialize Hardware
lightStatus = mraa.Gpio(36) #edisonPin -> 14
lightStatus.dir(mraa.DIR_OUT)
lightStatus.write(0)

statusArduino = mraa.Gpio(47) #edisonPin -> 49
statusArduino.dir(mraa.DIR_OUT)
statusArduino.write(0)

statusRaspPi = mraa.Gpio(46) #edisonPin -> 47
statusRaspPi.dir(mraa.DIR_OUT)
statusRaspPi.write(0)



# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected to Broker with result code: "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("LightStatus", 2), ("Status/Arduino", 2), ("Status/RaspPi", 2)])


   
# The callback for when a SUBSCRIBED message is received from the server.
def on_message(client, userdata, msg):
    print("Topic: " + msg.topic + " " + "Payload:" + str(msg.payload))
    if msg.topic == 'LightStatus':
         if msg.payload == 'TurnOn':
	      lightStatus.write(1)
         else: lightStatus.write(0)
    elif msg.topic == 'Status/Arduino':
         #global statusArduino
         if msg.payload == 'online':
              statusArduino.write(1)         
	 else:
              statusArduino.write(0)
    elif msg.topic == 'Status/RaspPi':
         #global statusRaspPi    
	 if msg.payload == 'online':
              statusRaspPi.write(1)
         else:
              statusRaspPi.write(0)


# create Client object and connect to broker
client = mqtt.Client() 
client.on_connect = on_connect
client.on_message = on_message
client.connect(brokerIP, brokerPort, keepAlive) #connect to broker as client
client.loop_forever()

          

