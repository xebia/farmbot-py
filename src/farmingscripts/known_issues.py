from farmbot.bot import create_farmbot
from farmbot.log import configure_logger
import logging

bot = create_farmbot('./config.json')
configure_logger(bot.cfg)

logger = logging.getLogger(__name__)

try:
    # Issue 1
    # The corpus says that kind 'home' is the message to use, but in practice it's 'find_home'.
    # Corpus: https://github.com/FarmBot/farmbot-js/blob/master/src/farmbot.ts Line 155-163

    # Issue 2
    # The 'home' message ignores the axis parameter and always goes to (0, 0, 0)
    # bot.go_home(Axis.z)

    # Issue 3
    # A 'read_pin' message responds with only an 'rpc_ok', there's no way to read the response for pin 63.
    # A read pin message needs to wait for a log item that corresponds to what was read.
    logger.debug(f"The result of 'reading' pin 63 is: {bot.tool_mounted()}")

finally:
    bot.stop()
