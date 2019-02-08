import json
from enum import Enum, unique

DEVICE_ID = 'device_id'
PLOTS = 'plots'
SEEDER_PLANT_HEIGHT = 'seeder_plant_height'
TOKEN = 'token'
TOOL_BAY = 'tool_bay'
TOOL_BAY_CLEARANCE = 'tool_bay_clearance'
XYZ = 'xyz'


@unique
class Peripheral(Enum):
    Lighting = 'lighting'
    Water = 'water'
    Vacuum = 'vacuum'
    Peripheral_4 = 'peripheral_4'
    Peripheral_5 = 'peripheral_5'


@unique
class ToolBay(Enum):
    Sensor = 'sensor'
    Weeder = 'weeder'
    Watering_Nozzle = 'watering_nozzle'
    Seeder = 'seeder'
    SeedBin = 'seed_bin'
    SeedTrayA1 = 'seed_tray_a1'
    SeedTrayD4 = 'seed_tray_d4'


class FarmBotConfiguration(object):
    def __init__(self, config_file_name):
        with open(config_file_name, 'r') as f:
            self.cfg = json.load(f)

    def __getitem__(self, key):
        return self.cfg[key]

    def get(self, key, default):
        return self.cfg.get(key, default)

    @property
    def device_id(self):
        return self.cfg[DEVICE_ID]

    @property
    def token(self):
        return self.cfg[TOKEN]

    @property
    def tool_bay_clearance(self):
        return self.cfg[TOOL_BAY_CLEARANCE]

    def location_of(self, item: ToolBay):
        if isinstance(item, Enum):
            item = item.value
        return self.cfg[TOOL_BAY][item][XYZ]

