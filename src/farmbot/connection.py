import json
import time
from farmbot.config import FarmBotConfiguration

from paho.mqtt import client as mqtt

DEFAULT_MQTT_PORT = 1883
DEFAULT_MQTT_KEEP_ALIVE = 60


class FarmBotConnection(object):
    def __init__(self, config: FarmBotConfiguration):
        self.cfg = config
        self.client = mqtt.Client()
        self.client.username_pw_set(self.cfg.device_id, self.cfg.token)
        self.client.connected_flag = False
        self.started = False

    def send_command(self, rpc_request, wait_time=10):
        """Creates a blocking call to the Farmbot, waiting for it to complete the command before returning.
        It blocks by reading the incoming messages from_device and waiting for an rpc_ok message with the right uuid."""
        command_done = False

        def on_message(client, userdata, msg):
            nonlocal command_done
            json_message = json.loads(msg.payload)
            print(json_message)
            if json_message['kind'] == 'rpc_ok' and json_message['args']['label'] == rpc_request.uuid:
                command_done = True
                print(f"Command {rpc_request.uuid} done.")

        self.client.on_message = on_message
        self.start()
        self.client.publish(f"bot/{self.cfg.device_id}/from_clients", rpc_request.to_json())
        print(f"Sent command {rpc_request.to_json()}")

        counter = 0
        while not command_done and counter <= (wait_time * 100):
            time.sleep(0.01)
            counter += 1

    def start(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                client.connected_flag = True
                print(f"Connected to {self.cfg.device_id}!")
                client.subscribe(f"bot/{self.cfg.device_id}/from_device")
            else:
                print("Bad connection Returned code=", rc)

        if not self.started:
            print("Connecting...")
            self.client.on_connect = on_connect
            url = self.cfg['broker_url']
            port = self.cfg.get('broker_port', DEFAULT_MQTT_PORT)
            keep_alive = self.cfg.get('broker_keepalive', DEFAULT_MQTT_KEEP_ALIVE)
            self.client.connect(url, port, keep_alive)
            self.client.loop_start()
            while not self.client.connected_flag:
                print("Waiting to connect...")
                time.sleep(1)
            self.started = True

    def stop(self):
        if self.started:
            self.client.loop_stop()
            self.client.disconnect()
            self.started = False
