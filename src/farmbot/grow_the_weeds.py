from farmbot.bot import FarmBot, Axis
from farmbot.connection import FarmBotConnection
from farmbot.config import FarmBotConfiguration, ToolBay

cfg = FarmBotConfiguration('./config.json')
bot = FarmBot(cfg, FarmBotConnection(cfg))
try:
    bot.set_lights(True)
    bot.go_home(Axis.all)
    bot.pick_up_tool(ToolBay.Watering_Nozzle)
    bot.water((1160, 520), 1, -200)
    bot.water_on(1)
    bot.water_on(1)
    bot.water_on(1)
    bot.return_tool(ToolBay.Watering_Nozzle)
    bot.go_home(Axis.all)
    bot.set_lights(False)
    bot.blink_lights(3)
finally:
    bot.stop()
