from farmbot.bot import FarmBot, Axis
from farmbot.connection import FarmBotConnection
from farmbot.config import FarmBotConfiguration, ToolBay

cfg = FarmBotConfiguration('./config.json')
bot = FarmBot(cfg, FarmBotConnection(cfg))
try:
    # Issue 1
    # The corpus says that kind 'home' is the message to use, but in practice it's 'find_home'.
    # Corpus: https://github.com/FarmBot/farmbot-js/blob/master/src/farmbot.ts Line 155-163

    # Issue 2
    # The 'home' message ignores the axis parameter and always goes to (0, 0, 0)

    # bot.go_home(Axis.z)

    # Issue 3
    # A 'read_pin' message responds with only an 'rpc_ok', there's no way to read the response for pin 63.

    bot.read_pin(63)
    # bot.read_status()

    # After these two commands the only info is:
    # bot/device_xxxx/logs {'z': -329.44, 'y': 692.0, 'x': 2635.2, 'verbosity': 1, 'type': 'success', 'patch_version': 13, 'minor_version': 4, 'message': 'Tool Verification value is 1 (digital)', 'major_version': 6, 'created_at': 1547931354, 'channels': []}
    # A string with 'tool verification is...'.

finally:
    bot.stop()
