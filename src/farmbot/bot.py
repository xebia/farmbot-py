import time
import logging
from enum import Enum, unique
from farmbot.config import FarmBotConfiguration, ToolBay, Peripheral, Zone
from farmbot.connection import FarmBotConnection
from farmbot.celery import *

TOOL_VERIFICATION_PIN = 63

logger = logging.getLogger(__name__)


@unique
class Axis(Enum):
    x = 'x'
    y = 'y'
    z = 'z'
    all = 'all'


def max_height(xyz):
    return xyz[0], xyz[1], 0


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

    def blink_lights(self, nr_times):
        for i in range(nr_times):
            self.set_lights(True)
            self.set_lights(False)

    def set_lights(self, on_off):
        self.write_pin(Peripheral.Lighting, 1 if on_off else 0)

    def pick_up_tool(self, tool: ToolBay):
        """Safe move to tool and move out of tool bay."""
        self.safe_move(self.cfg.location_of(tool))
        self.move_relative(x=self.cfg.tool_bay_clearance)

    def plant_seed(self, seed_source, destination):
        self.safe_move(self.cfg.location_of(seed_source))
        self.write_pin(Peripheral.Vacuum, 1)
        self.safe_move(destination)
        self.write_pin(Peripheral.Vacuum, 0)
        self.go_home(Axis.z)

    def reset(self):
        self.write_pin(Peripheral.Water, 0)
        self.write_pin(Peripheral.Vacuum, 0)
        self.set_lights(False)
        self.go_home(Axis.all)

    def return_tool(self, tool):
        """Safe move to clearance location, and then push the tool into the tool bay."""
        x, y, z = self.cfg.location_of(tool)
        x_clear = x + self.cfg.tool_bay_clearance
        self.safe_move((x_clear, y, z))
        self.move_absolute(self.cfg.location_of(tool))
        self.move_relative(z=100)

    def safe_move(self, coords):
        """Go up to max height, move horizontally over to x, y and then go down to z."""
        self.go_home(Axis.z)
        self.move_absolute(max_height(coords))
        self.move_absolute(coords)

    def verify_tool(self):
        # TODO This does not work yet. No idea how to get a pin value back.
        self.read_pin(TOOL_VERIFICATION_PIN)

    def water_on(self, duration):
        self.write_pin(Peripheral.Water, 1)
        # TODO A more robust way to space the off command due to network lag. This works well, though...
        time.sleep(duration)
        self.write_pin(Peripheral.Water, 0)

    def water(self, xy, duration, z=0, safe_move=True):
        # TODO Can we detect which tool is currently in the tool mount?
        # TODO if not current tool == watering nozzle then pick it up
        # self.pick_up_tool(ToolBay.Watering_Nozzle)
        logger.debug(f"Watering ({xy[0]}, {xy[1]}, {z})  for {duration} seconds.")
        if safe_move:
            self.safe_move((xy[0], xy[1], z))
        else:
            self.move_absolute((xy[0], xy[1], z))
        self.water_on(duration)

    def water_multiple(self, water_plan):
        for step in water_plan:
            self.water(step[0], step[1])

    def water_zone(self, zone: Zone, height, step_distance=100, water_duration=1):
        self.safe_move((zone.x_min, zone.y_min, height))
        # Preload the watering hose
        self.water_on(2)
        forward_direction = True
        for x in range(zone.x_min, zone.x_max, step_distance):
            if forward_direction:
                y_from, y_to = zone.y_min, zone.y_max
            else:
                y_from, y_to = zone.y_max, zone.y_min
            y_delta = step_distance if forward_direction else -step_distance
            for y in range(y_from, y_to, y_delta):
                self.water((x, y), water_duration, z=height, safe_move=False)
            forward_direction = not forward_direction

    # ------------------------------------------------------------ Basic Commands (in alphabetic order)

    def calibrate(self, axis: Axis):
        self._send_command(Calibrate(axis.value))

    def dump_info(self):
        self._send_command(DumpInfo())

    def execute_sequence_id(self, sequence_id):
        self._send_command(ExecuteSequenceID(sequence_id))

    def go_home(self, axis: Axis, speed=100):
        if axis == Axis.all:
            self.go_home(Axis.z, speed)
            self.move_absolute((0, 0, 0), speed)
        else:
            self._send_command(GoHome(axis.value, speed))

    def move_absolute(self, coords, speed=100):
        self._send_command(MoveAbsolute(coords, speed=speed))

    def move_relative(self, x=0, y=0, z=0, speed=100):
        self._send_command(MoveRelative(x, y, z, speed))

    def read_pin(self, pin):
        self._send_command(ReadPin(pin))

    def read_status(self):
        self._send_command(ReadStatus())

    def take_photo(self):
        self._send_command(TakePhoto())

    def write_pin(self, pin: Peripheral, value):
        assert type(pin) is Peripheral
        pin_nr = self.cfg['peripherals'][pin.value]
        self._send_command(WritePin(int(pin_nr), value))


if __name__ == '__main__':
    cfg = FarmBotConfiguration('./config.json')
    bot = FarmBot(cfg, FarmBotConnection(cfg))
    try:
        print("Hello Farmbot! Blinking the lights!")
        bot.blink_lights(3)
    finally:
        bot.stop()
