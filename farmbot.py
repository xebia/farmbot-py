import json
import time
import uuid
import paho.mqtt.client as mqtt
from config import my_device_id, my_token

ALLOWED_AXIS = ('x', 'y', 'z', 'all')


def coordinate(x, y, z):
    return cmd('coordinate', {'x': x, 'y': y, 'z': z})


def cmd(kind, args):
    return {'kind': kind, 'args': args}


class RPCRequest(object):
    def __init__(self, kind, args):
        self.command = cmd(kind, args)
        self._uuid = str(uuid.uuid4())

    def to_json(self):
        return json.dumps({
            'kind': 'rpc_request',
            'args': {'label': self._uuid},
            'body': [self.command]
        })

    @property
    def uuid(self):
        return self._uuid


class FarmBot(object):
    def __init__(self, conn):
        self.connection = conn

    def move_absolute(self, x, y, z, speed):
        self._send_command('move_absolute',
                                  {'location': coordinate(x, y, z),
                                   'offset': coordinate(0, 0, 0),
                                   'speed': speed})

    def move_relative(self, x, y, z, speed):
        self._send_command('move_relative', {'x': x, 'y': y, 'z': z, 'speed': speed})

    def execute_sequence_id(self, sequence_id):
        self._send_command('execute', {'sequence_id': sequence_id})

    def write_pin(self, pin_nr, value):
        self._send_command('write_pin', {'pin_number': pin_nr, 'pin_value': value, 'pin_mode': 0})

    def read_pin(self, pin_nr):
        self._send_command('read_pin', {'pin_number': pin_nr, 'label': "---", 'pin_mode': 0})

    def take_photo(self):
        self._send_command('take_photo', {})

    def dump_info(self):
        self._send_command('dump_info', {})

    def calibrate(self, axis):
        if axis in ALLOWED_AXIS:
            self._send_command('calibrate', {'axis': axis})
        else:
            print(f"Can't calibrate on axis {axis}")

    def _send_command(self, kind, args):
        self.connection.send_command(RPCRequest(kind, args))

    def stop(self):
        self.connection.stop()


class FarmBotConnection(object):
    def __init__(self, device_id, token):
        self.client = mqtt.Client()
        self.client.username_pw_set(device_id, token)
        self.client.connected_flag = False
        self.started = False

    def send_command(self, rpc_request, wait_time=10):
        """Creates a blocking call to the Farmbot, waiting for it to complete the command before returning."""
        command_done = False

        def on_message(client, userdata, msg):
            nonlocal command_done
            json_message = json.loads(msg.payload)
            if json_message['kind'] == 'rpc_ok' and json_message['args']['label'] == rpc_request.uuid:
                command_done = True
                print(f"Command {rpc_request.uuid} done.")
            else:
                print(json_message)

        self.client.on_message = on_message
        self.start()
        self.client.publish(f"bot/{my_device_id}/from_clients", rpc_request.to_json())
        print(f"Sent command {rpc_request.to_json()}")

        counter = 0
        while not command_done and counter <= (wait_time * 100):
            time.sleep(0.01)
            counter += 1

    def start(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                client.connected_flag = True
                print(f"Connected to {my_device_id}!")
                client.subscribe(f"bot/{my_device_id}/from_device")
            else:
                print("Bad connection Returned code= ", rc)

        if not self.started:
            print("Connecting...")
            self.client.on_connect = on_connect
            self.client.connect("brisk-bear.rmq.cloudamqp.com", 1883, 60)
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


if __name__ == '__main__':
    bot = FarmBot(FarmBotConnection(my_device_id, my_token))
    try:
        # bot.execute_sequence_id(13729)
        bot.write_pin(7, 1)
        bot.write_pin(7, 0)
        # bot.calibrate('all')
        # bot.move_absolute(2000, 0, 0, 100)
        # bot.read_pin(7)
        # bot.take_photo()
        # bot.move_relative(0, 0, 10, 100)
    finally:
        bot.stop()
