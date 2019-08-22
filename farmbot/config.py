import json
from enum import Enum, unique

DEVICE_ID = 'device_id'
PERIPHERALS = 'peripherals'
PLOTS = 'plots'
TOKEN = 'token'
TOOL_BAYS = 'tool_bays'
TOOL_BAY_CLEARANCE = 'tool_bay_clearance'
XYZ = 'xyz'
ZONES = 'zones'

# SEEDER_PLANT_HEIGHT = 'seeder_plant_height'


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


class Zone(object):
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates

    @property
    def x_min(self):
        return self.coordinates["x"][0]

    @property
    def x_max(self):
        return self.coordinates["x"][1]

    @property
    def y_min(self):
        return self.coordinates["y"][0]

    @property
    def y_max(self):
        return self.coordinates["y"][1]


class FarmBotConfiguration(object):
    def __init__(self, config_file_name):
        with open(config_file_name, 'r') as f:
            self.cfg = json.load(f)
        self.zones = dict()
        for zone_id in self.cfg[ZONES]:
            zone = self.cfg[ZONES][zone_id]
            self.zones[zone_id] = Zone(zone_id, zone)

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

    def peripheral_id(self, peripheral):
        return self.cfg['peripherals'][peripheral.value]

    def location_of(self, item: ToolBay):
        if isinstance(item, Enum):
            item = item.value
        return self.cfg[TOOL_BAYS][item][XYZ]

    def pin_number_of(self, peripheral: Peripheral):
        return self.cfg[PERIPHERALS][peripheral.value]

