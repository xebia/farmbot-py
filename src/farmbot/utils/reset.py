from farmbot.bot import create_farmbot

bot = create_farmbot('./config.json')
try:
    bot.reset()
finally:
    bot.stop()
