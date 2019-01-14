import time
from enum import Enum, unique
from farmbot.config import *
from farmbot.connection import FarmBotConnection
from farmbot.celery import *


@unique
class Axis(Enum):
    x = 'x'
    y = 'y'
    z = 'z'
    all = 'all'


def max_height(coord):
    return coord[0], coord[1], 0


class FarmBot(object):
    """Abstraction of the FarmBot with a higher level interface for ease of programming."""
    def __init__(self, config: FarmBotConfiguration, connection: FarmBotConnection):
        self.cfg = config
        self.connection = connection

    def _send_command(self, command):
        self.connection.send_command(RPCRequest(command))

    def stop(self):
        self.connection.stop()

    # ------------------------------------------------------------ Compound Commands

    def safe_move(self, coords):
        """Go up to max height, move horizontally over to x, y and then go down to z."""
        self.go_home(Axis.z)
        self.move_absolute(max_height(coords))
        self.move_absolute(coords)

    def pick_up_tool(self, tool):
        """Safe move to tool and move out of tool bay.

        Params:
            tool    Instance farmbot.farmbot.Tool"""
        self.safe_move(self.cfg.location_of(tool))
        self.move_relative(x=self.cfg.tool_bay_clearance)

    def return_tool(self, tool):
        x, y, z = self.cfg.location_of(tool)
        x_clear = x + self.cfg.tool_bay_clearance
        self.safe_move((x_clear, y, z))
        self.move_absolute(self.cfg.location_of(tool))
        self.move_relative(z=-100)

    def water_multiple(self, water_plan):
        for step in water_plan:
            self.water(step[0], step[1])

    def water(self, xy, duration):
        # TODO Can we detect which tool is currently in the tool mount?
        # TODO if not current tool == watering nozzle then pick it up
        self.pick_up_tool(ToolBay.Watering_Nozzle)
        self.safe_move((xy[0], xy[1], 0))
        self.write_pin(Peripheral.Water, 1)
        # TODO A more robust way to space the off command due to network lag.
        time.sleep(duration)
        self.write_pin(Peripheral.Water, 0)

    def plant_seed(self, seed_source, destination):
        self.pick_up_tool(ToolBay.Seeder)
        self.safe_move(self.cfg.location_of(seed_source))
        self.write_pin(Peripheral.Vacuum, 1)
        self.safe_move(destination)
        self.write_pin(Peripheral.Vacuum, 0)
        self.go_home(Axis.z)

    def blink_lights(self, nr_times):
        for i in range(nr_times):
            self.write_pin(Peripheral.Lighting, 1)
            self.write_pin(Peripheral.Lighting, 0)

    # ------------------------------------------------------------ Basic Commands

    def go_home(self, axis: Axis):
        self._send_command(GoHome(axis.value))

    def move_absolute(self, coords, speed=100):
        self._send_command(MoveAbsolute(coords, speed=speed))

    def move_relative(self, x=0, y=0, z=0, speed=100):
        self._send_command(MoveRelative(x, y, z, speed))

    def execute_sequence_id(self, sequence_id):
        self._send_command(ExecuteSequenceID(sequence_id))

    def write_pin(self, pin, value):
        if type(pin) is Peripheral:
            pin = pin.value
        self._send_command(WritePin(pin, value))

    def read_pin(self, pin):
        if type(pin) is Peripheral:
            pin = pin.value
        self._send_command(ReadPin(pin))

    def take_photo(self):
        self._send_command(TakePhoto())

    def dump_info(self):
        self._send_command(DumpInfo())

    def calibrate(self, axis: Axis):
        self._send_command(Calibrate(axis.value))


if __name__ == '__main__':
    cfg = FarmBotConfiguration('./config.json')
    bot = FarmBot(cfg, FarmBotConnection(cfg))
    try:
        print("Hello Farmbot! Blinking the lights!")
        bot.blink_lights(3)
    finally:
        bot.stop()
