from farmbot.bot import create_farmbot, Axis
from farmbot.config import ToolBay

bot = create_farmbot('./config.json')
try:
    bot.set_lights(True)
    bot.go_home(Axis.all)
    if not bot.tool_mounted():
        bot.pick_up_tool(ToolBay.Watering_Nozzle)
    bot.water((1160, 520), 1, -200)
    bot.water_on(1)
    bot.water_on(1)
    bot.water_on(1)
    bot.return_tool(ToolBay.Watering_Nozzle)
    bot.reset()
    bot.blink_lights(3)
finally:
    bot.stop()
