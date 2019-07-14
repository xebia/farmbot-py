from farmbot.bot import create_farmbot, Axis
from farmbot.config import ToolBay

bot = create_farmbot('./config.json')
try:
    bot.set_lights(True)
    bot.go_home(Axis.all)
    if not bot.tool_mounted():
        bot.pick_up_tool(ToolBay.Watering_Nozzle)
#    bot.water_zone(cfg.zones["6"], -250)
#    bot.water_zone(cfg.zones["5"], -200)
    bot.water_zone(bot.cfg.zones["3"], -200)
#    bot.water_zone(cfg.zones["4"], -250)
#    bot.water_zone(cfg.zones["2"], -250)
#    bot.water_zone(cfg.zones["1"], 0)

    bot.return_tool(ToolBay.Watering_Nozzle)
    bot.reset()
    bot.blink_lights(3)
finally:
    bot.stop()
