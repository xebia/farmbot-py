import json
from farmbot.bot import FarmBot, Axis
from farmbot.connection import FarmBotConnection
from farmbot.config import FarmBotConfiguration, ToolBay


class GardenBedConfig(object):
    def __init__(self, file_name):
        with open(file_name) as f:
            self._data = json.load(f)

    @property
    def bed_height(self):
        return self._data['bed_height']

    @property
    def plots(self):
        return self._data['plots']


class GardenBed(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.cfg = config

    def water_plots(self):
        for plot in self.cfg.plots:
            self.water(plot)

    def water(self, plot):
        for coord in plot['coords']:
            self.bot.water(coord, int(plot['water_time']))

    def seed(self, plot):
        self.bot.pick_up_tool(ToolBay.Seeder)
        self.bot.plant_seed(ToolBay.SeedTrayA1, plot)
        self.bot.return_tool(ToolBay.Seeder)

    def seed_all(self, plots):
        self.bot.pick_up_tool(ToolBay.Seeder)
        for plot in plots:
            self.bot.plant_seed(ToolBay.SeedTrayA1, plot)
        self.bot.return_tool(ToolBay.Seeder)

    def water_all(self, plots):
        self.bot.pick_up_tool(ToolBay.Watering_Nozzle)
        for plot in plots:
            self.water(plot)
        self.bot.return_tool(ToolBay.Watering_Nozzle)


cfg = FarmBotConfiguration('./config.json')
bot = FarmBot(cfg, FarmBotConnection(cfg))
bedconfig = GardenBedConfig('./garden_bed.json')
bed = GardenBed(bot, bedconfig)
try:
    bed.water_all(bedconfig.plots)
    bot.go_home(Axis.z)
    bot.go_home(Axis.x)
finally:
    bot.stop()

