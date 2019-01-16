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
    # A 'read_pin' message responds with an
    # Unknown syncable: Elixir.Farmbot.Asset.SensorReading error message

    # {'kind': 'rpc_error', 'comment': None, 'body': [{'kind': 'explanation', 'comment': None, 'body': [],
    #       'args': {'message': 'Unknown syncable: Elixir.Farmbot.Asset.SensorReading'}}],
    #       'args': {'label': 'f47ebec0-fe15-42b6-9424-a4f78c79fbcb'}}

    bot.verify_tool()
finally:
    bot.stop()
