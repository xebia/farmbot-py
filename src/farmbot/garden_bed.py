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
    def plots(self, include_seeder_height=True):
        if include_seeder_height:
            return [(p[0], p[1], self._data['bed_height']) for p in self._data['plots']]
        else:
            return self.cfg['plots']


class GardenBed(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.cfg = config

    def water_plots(self):
        for plot in self.cfg.plots:
            self.water(plot)

    def water(self, plot):
        self.bot.pick_up_tool(ToolBay.Watering_Nozzle)
        self.bot.water(plot, 6)

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
            self.bot.water(plot, 6)


cfg = FarmBotConfiguration('./config.json')
bot = FarmBot(cfg, FarmBotConnection(cfg))
bedconfig = GardenBedConfig('./garden_bed.json')
bed = GardenBed(bot, bedconfig)
try:
    # bed.seed_all(bedconfig.plots)
    bed.water_all(bedconfig.plots)
finally:
    bot.stop()

    # bot.calibrate(Axis.all)
    # bot.pick_up_tool(ToolBay.Watering_Nozzle)
    # bot.water((1140, 110), 3)
    # bot.water((820, 520), 3)
    # bot.verify_tool()
    # bot.dump_info()
    # bot.read_stats()
    # bot.return_tool(ToolBay.Watering_Nozzle)

