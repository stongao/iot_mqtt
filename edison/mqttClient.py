import paho.mqtt.client as mqtt
import sys

brokerIP = '127.0.0.1' #mqtt broker IP address (PC1)
brokerPort = 1883 #mqtt broker Port number
keepAlive = 60 #client keep alive time (sec)
bindAddress = '0.0.0.0' #bind address

global latestMessage
global oldMessage

latestMessage = ''
oldMessage = ''

# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("example", qos=2)
   

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    global latestMessage 
    latestMessage = str(msg.payload)
    print latestMessage
client = mqtt.Client(client_id="edison", 
                     clean_session=True, 
                     userdata=None, 
                     protocol="MQTTv311")

client.on_connect = on_connect
client.on_message = on_message

client.connect(brokerIP, brokerPort, keepAlive, bindAddress) #connect to broker as client

# loop_forever() is a blocking statement holding the main thread
# Using loop_start()/loop_stop() -> runs a thread in background to call loop()
# automatically

client.loop_start()


oldMessage = latestMessage

while True:
     if oldMessage != latestMessage:
          print "message changed"
          oldMessage = latestMessage 
#     print latestMessage
     if latestMessage == "quit":
          print "in quit loop"
          client.loop_stop()
          client.disconnect()
          sys.exit()


