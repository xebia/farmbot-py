from farmbot.bot import FarmBot
from farmbot.connection import FarmBotConnection
from farmbot.config import FarmBotConfiguration
from farmbot.log import configure_logger

cfg = FarmBotConfiguration('./config.json')
bot = FarmBot(cfg, FarmBotConnection(cfg))
configure_logger(cfg)
try:
    bot.reset()
finally:
    bot.stop()
