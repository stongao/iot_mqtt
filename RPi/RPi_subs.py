import paho.mqtt.client as mqtt

LIGHT_SENSOR_TOPIC = "arduino/lightSensor"
THRESHOLD_TOPIC = "arduino/threshold"

LIGHT_STATUS = "RPi/LightStatus"

RPI_STATUS = "Status/RPi"

light_sensor_value = 0
threshold_value = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
#    client.subscribe("$SYS/#")
    client.subscribe("sensor/temp")
	
    # Arduino Light Sensor and the threshold values.
    client.subscribe(LIGHT_SENSOR_TOPIC,2)
    client.subscribe(THRESHOLD_TOPIC,2)


    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
#    print(msg.topic+" "+str(msg.payload))

    print("Topic is:" + msg.topic)

    if msg.topic == LIGHT_SENSOR_TOPIC:
        light_sensor_value = msg.payload     

    elif msg.topic == THRESHOLD_TOPIC:
        threshold_value = msg.payload

        if light_sensor_value >= threshold_value:
	    client.publish(LIGHT_STATUS, payload = "TurnOn", qos = 2, retain = True)
        end

    else:
        print("Invalid Topic:" + msg.topic)
    end


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.139.59.228", 1883, 60)
client.will_set(RPI_STATUS,payload = "offline", qos = 2, retain = True)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()