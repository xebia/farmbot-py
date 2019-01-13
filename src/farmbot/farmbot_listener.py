import json
import paho.mqtt.client as mqtt
from farmbot.config import my_device_id, my_token


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt_prefix = f"bot/{my_device_id}"
    client.subscribe(f"{mqtt_prefix}/status")
    client.subscribe(f"{mqtt_prefix}/logs")
    client.subscribe(f"{mqtt_prefix}/from_clients")
    client.subscribe(f"{mqtt_prefix}/from_device")


ping_count = 0


def on_message(client, userdata, msg):
    global ping_count
    json_message = json.loads(msg.payload)
    # msg.topic
    if json_message["args"]["label"] != "ping":
        print(str(msg.topic) + " " + str(json_message))
    else:
        if ping_count >= 10:
            print(str(msg.topic) + " " + str(json_message))
            ping_count = 0
        ping_count += 1


client = mqtt.Client()
client.username_pw_set(my_device_id, my_token)

# Attach event handlers:
client.on_connect = on_connect
client.on_message = on_message

# Finally, connect to the server:
client.connect("brisk-bear.rmq.cloudamqp.com", 1883, 60)

client.loop_forever()
