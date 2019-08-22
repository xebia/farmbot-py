import unittest
from farmbot.bot import FarmBot, Axis
from farmbot.connection import FarmBotConnection
from farmbot.celery import *
from farmbot.config import FarmBotConfiguration, Peripheral, ToolBay

from farmbottest.mockconnection import MockReplayFarmBotConnection


class TestFarmbot(unittest.TestCase):
    def setUp(self):
        self.cfg = FarmBotConfiguration('./config.json')
        self.conn = MockReplayFarmBotConnection(self.cfg)
        self.bot = FarmBot(self.cfg, self.conn)

    def test_blink_lights(self):
        # Note that the WritePin is CeleryScript and does not (should not) know the Peripheral type
        self.conn.add_expected_command(WritePin(self.cfg.pin_number_of(Peripheral.Lighting), 1))
        self.conn.add_expected_command(WritePin(self.cfg.pin_number_of(Peripheral.Lighting), 0))

        self.bot.write_pin(Peripheral.Lighting, 1)
        self.bot.write_pin(Peripheral.Lighting, 0)

        self.assertTrue(self.conn.commands_empty)

    def test_safe_move(self):
        self.conn.add_expected_command(GoHome(Axis.z))
        self.conn.add_expected_command(MoveAbsolute((100, 100, 0)))
        self.conn.add_expected_command(MoveAbsolute((100, 100, -100)))

        self.bot.safe_move((100, 100, -100))

        self.assertTrue(self.conn.commands_empty)

    def test_plant_seed(self):
        seed_bin_location = self.cfg.location_of(ToolBay.SeedBin)
        target_location = (100, 100, -104)

        self.conn.add_expected_command(GoHome(Axis.z))
        self.conn.add_expected_command(MoveAbsolute(max_height(seed_bin_location)))
        self.conn.add_expected_command(MoveAbsolute(seed_bin_location))
        self.conn.add_expected_command(WritePin(self.cfg.pin_number_of(Peripheral.Vacuum), 1))
        self.conn.add_expected_command(GoHome(Axis.z))
        self.conn.add_expected_command(MoveAbsolute(max_height(target_location)))
        self.conn.add_expected_command(MoveAbsolute(target_location))
        self.conn.add_expected_command(WritePin(self.cfg.pin_number_of(Peripheral.Vacuum), 0))
        self.conn.add_expected_command(GoHome(Axis.z))

        self.bot.plant_seed(ToolBay.SeedBin, (100, 100, -104))

        self.assertTrue(self.conn.commands_empty)

    def test_execute_sequence_id(self):
        self.conn.add_expected_command(ExecuteSequenceID(13729))

        self.bot.execute_sequence_id(13729)

        self.assertTrue(self.conn.commands_empty)

    def test_calibrate_all(self):
        self.conn.add_expected_command(Calibrate(Axis.all))

        self.bot.calibrate(Axis.all)

        self.assertTrue(self.conn.commands_empty)

    def test_move_absolute(self):
        self.conn.add_expected_command(MoveAbsolute((1, 2, 3), speed=50))

        self.bot.move_absolute((1, 2, 3), speed=50)

        self.assertTrue(self.conn.commands_empty)

    def test_read_pin(self):
        self.conn.add_expected_command(ReadPin(self.cfg.pin_number_of(Peripheral.Peripheral_4)))

        self.bot.read_pin(self.cfg.pin_number_of(Peripheral.Peripheral_4))

        self.assertTrue(self.conn.commands_empty)

    def test_take_photo(self):
        self.conn.add_expected_command(TakePhoto())

        self.bot.take_photo()

        self.assertTrue(self.conn.commands_empty)

    def test_move_relative(self):
        self.conn.add_expected_command(MoveRelative(x=100, y=20, speed=50))

        self.bot.move_relative(x=100, y=20, speed=50)

        self.assertTrue(self.conn.commands_empty)



