import paho.mqtt.client as mqtt

LIGHT_SENSOR_TOPIC = "lightSensor"
THRESHOLD_TOPIC = "threshold"

LIGHT_STATUS = "LightStatus"

RPI_STATUS = "Status/RaspPi"

light_sensor_value = 0
threshold_value = 0

is_led_on = False


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #    client.subscribe("$SYS/#")
    # client.subscribe("sensor/temp")

    # Arduino Light Sensor and the threshold values.
    client.subscribe(LIGHT_SENSOR_TOPIC, 2)
    client.subscribe(THRESHOLD_TOPIC, 2)
    client.subscribe(LIGHT_STATUS, 2)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #    print(msg.topic+" "+str(msg.payload))

    print("Topic is:" + msg.topic + " With Value:" + msg.payload)
    global is_led_on
    global light_sensor_value
    global threshold_value

    if msg.topic == LIGHT_SENSOR_TOPIC:
        light_sensor_value = msg.payload

    elif msg.topic == THRESHOLD_TOPIC:
        threshold_value = msg.payload

        if int(light_sensor_value) >= int(threshold_value):
            if not is_led_on:
                client.publish(LIGHT_STATUS, payload="TurnOn", qos=2, retain=True)
        else:
            if is_led_on:
                client.publish(LIGHT_STATUS, payload="TurnOff", qos=2, retain=True)

    elif msg.topic == LIGHT_STATUS:
        if msg.payload == "TurnOn":
            is_led_on = True
        elif msg.payload == "TurnOff":
            is_led_on = False

        print("LED Status:" + str(is_led_on))

    else:
        print("Invalid Topic:" + msg.topic)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("10.139.59.228", 1883, 60)
client.will_set(RPI_STATUS, payload="offline", qos=2, retain=True)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
