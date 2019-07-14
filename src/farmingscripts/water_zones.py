from farmbot.bot import FarmBot, Axis
from farmbot.connection import FarmBotConnection
from farmbot.config import FarmBotConfiguration, ToolBay

cfg = FarmBotConfiguration('./config.json')
bot = FarmBot(cfg, FarmBotConnection(cfg))
try:
    bot.set_lights(True)
#    bot.go_home(Axis.all)
#    bot.pick_up_tool(ToolBay.Watering_Nozzle)

#    bot.water_zone(cfg.zones["6"], -250)
#    bot.water_zone(cfg.zones["5"], -200)
    bot.water_zone(cfg.zones["3"], -200)
#    bot.water_zone(cfg.zones["4"], -250)
#    bot.water_zone(cfg.zones["2"], -250)
#    bot.water_zone(cfg.zones["1"], 0)

    bot.return_tool(ToolBay.Watering_Nozzle)
    bot.go_home(Axis.all)
    bot.set_lights(False)
    bot.blink_lights(3)
finally:
    bot.stop()
