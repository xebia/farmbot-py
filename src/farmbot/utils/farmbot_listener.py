import logging
import json
import paho.mqtt.client as mqtt
from farmbot.config import FarmBotConfiguration
from farmbot.log import configure_logger


REPORT_PING_ONCE_PER = 10

cfg = FarmBotConfiguration('./config.json')
configure_logger(cfg)

logger = logging.getLogger(__name__)

logger.info(f"Only printing pings once every {REPORT_PING_ONCE_PER} times.")

ping_count = 0
prev_status = ""


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code " + str(rc))
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
        # Only report the status if it changes. It gets sent really often.
        stat = json.loads(msg.payload)
        # Ignore changes in fiddly values that change all the time without much effect.
        stat['location_data']['raw_encoders'] = ''
        stat['informational_settings']['wifi_level'] = 0
        if prev_status != stat:
            diffs = [i for i in range(len(prev_status)) if prev_status[i] != msg.payload[i]]
            print(diffs, [chr(msg.payload[i]) for i in diffs])
            print(str(msg.topic) + " " + str(json_message))
            prev_status = stat
    else:
        print(str(msg.topic) + " " + str(json_message))


mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(cfg.device_id, cfg.token)

# Attach event handlers:
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Finally, connect to the server:
logger.info(f"Opening connection to URL: {cfg['broker_url']}, Port: {cfg['port']}, Keep-Alive: {cfg['keepalive']} seconds.")
mqtt_client.connect(cfg['broker_url'], cfg['port'], cfg['keepalive'])

mqtt_client.loop_forever()
