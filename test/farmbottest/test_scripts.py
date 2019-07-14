import unittest
from farmbot.bot import FarmBot
from farmbot.config import FarmBotConfiguration

from farmbottest.mockconnection import MockFarmBotConnection


class TestFarmbot(unittest.TestCase):
    def setUp(self):
        self.cfg = FarmBotConfiguration('./config.json')
        self.conn = MockFarmBotConnection(self.cfg)
        self.bot = FarmBot(self.cfg, self.conn)

    def test_water_zone(self):
        self.bot.water_zone(self.cfg.zones['6'], -200, step_distance=100, water_duration=0)
