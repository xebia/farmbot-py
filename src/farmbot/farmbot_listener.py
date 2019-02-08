import json
import paho.mqtt.client as mqtt
from farmbot.config import FarmBotConfiguration

REPORT_PING_ONCE_PER = 10

cfg = FarmBotConfiguration('./config.json')
ping_count = 0
prev_status = ""


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt_prefix = f"bot/{cfg.device_id}"
    client.subscribe(f"{mqtt_prefix}/status")
    client.subscribe(f"{mqtt_prefix}/logs")
    client.subscribe(f"{mqtt_prefix}/from_clients")
    client.subscribe(f"{mqtt_prefix}/from_device")


def on_message(client, userdata, msg):
    global prev_status
    global ping_count
    json_message = json.loads(msg.payload)
    if (msg.topic.endswith('from_device') or msg.topic.endswith('from_clients')) and (json_message["args"]["label"] == "ping"):
        # Only print a ping every once in a while
        if ping_count >= REPORT_PING_ONCE_PER:
            print(str(msg.topic) + " " + str(json_message))
            ping_count = 0
        ping_count += 1
    elif str(msg.topic)[-6:] == 'status':
        # Only report the status if it changes
        stat = json.loads(msg.payload)
        # Fiddly values that change all the time without much effect.
        stat['location_data']['raw_encoders'] = ''
        stat['informational_settings']['wifi_level'] = 0
        if prev_status != stat:
            diffs = [i for i in range(len(prev_status)) if prev_status[i] != msg.payload[i]]
            # print(diffs, [chr(msg.payload[i]) for i in diffs])
            print(str(msg.topic) + " " + str(json_message))
            prev_status = stat
    else:
        print(str(msg.topic) + " " + str(json_message))


client = mqtt.Client()
client.username_pw_set(cfg.device_id, cfg.token)

# Attach event handlers:
client.on_connect = on_connect
client.on_message = on_message

# Finally, connect to the server:
client.connect(cfg['broker_url'], cfg['port'], cfg['keepalive'])

client.loop_forever()
