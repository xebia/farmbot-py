import json
import time
import uuid
import paho.mqtt.client as mqtt
from config import my_device_id, my_token

ALLOWED_AXIS = ("x", "y", "z", "all")


def coordinate(x, y, z):
    return cmd("coordinate", {'x': x, 'y': y, 'z': z})


def rpc_request(command):
    return {
        "kind": "rpc_request",
        "args": {"label": str(uuid.uuid4())},
        "body": [command]
    }


def uuid_of_command(command):
    return command["args"]["label"]


def cmd(kind, args):
    return {"kind": kind, "args": args}


class Sequence(object):
    def __init__(self):
        pass


class FarmBot(object):
    def __init__(self, mqtt_client):
        self.client = mqtt_client

    def move_absolute(self, x, y, z, speed):
        return self._send_command(cmd('move_absolute',
                               {"location": coordinate(x, y, z),
                                "offset": coordinate(0, 0, 0),
                                'speed': speed}))

    def move_relative(self, x, y, z, speed):
        return self._send_command(cmd('move_relative', {'x': x, 'y': y, 'z': z, 'speed': speed}))

    def execute_sequence_id(self, sequence_id):
        return self._send_command(cmd('execute', {"sequence_id": sequence_id}))

    def write_pin(self, pin_nr, value):
        return self._send_command(cmd('write_pin', {"pin_number": pin_nr, "pin_value": value, "pin_mode": 0}))

    def read_pin(self, pin_nr):
        return self._send_command(cmd('read_pin', {"pin_number": pin_nr, "label": "---", "pin_mode": 0}))

    def take_photo(self):
        return self._send_command(cmd('take_photo', {}))

    def dump_info(self):
        return self._send_command(cmd('dump_info', {}))

    def calibrate(self, axis):
        if axis in ALLOWED_AXIS:
            return self._send_command(cmd("calibrate", {"axis": axis}))
        else:
            print(f"Can't calibrate on axis {axis}")

    def _send_command(self, command):
        req = rpc_request(command)
        json_payload = json.dumps(req)
        print("Sending" + json_payload)
        self.client.publish(f"bot/{my_device_id}/from_clients", json_payload)
        return uuid_of_command(req)


# An event handler for sending off data:
def on_connect(client, userdata, flags, rc):
    print("CONNECTED!")
    client.subscribe("bot/" + my_device_id + "/from_device")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


class FarmBotConnection(object):
    def __init__(self):
        # Connect to the broker...
        self.client = mqtt.Client()
        # ...using credentials from `token_generation_example.py`
        self.client.username_pw_set(my_device_id, my_token)

        # Attach event handler:
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect("brisk-bear.rmq.cloudamqp.com", 1883, 60)

    def run(self, hundreths=100):
        print("Here we go...")
        self.client.loop_start()
        try:
            counter = 0
            loop_flag = 1
            while loop_flag and counter < hundreths:
                time.sleep(.01)
                counter += 1
        finally:
            conn.client.disconnect()
            conn.client.loop_stop()


if __name__ == '__main__':
    conn = FarmBotConnection()
    bot = FarmBot(conn.client)
    # bot.execute_sequence_id(13729)
    # bot.write_pin(7, 0)
    # bot.calibrate("all")
    # bot.move_absolute(2000, 0, 0, 100)

    # bot.read_pin(7)
    # bot.take_photo()
    bot.move_relative(0, 0, 10, 100)
    conn.run(1000)
