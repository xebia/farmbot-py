import logging
from farmbot.config import FarmBotConfiguration

logger = logging.getLogger()

LOG_FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'


def configure_logger(cfg: FarmBotConfiguration):
    """Configure the file and console logging."""
    # Can also be done with os.environ.get("LOGLEVEL", "INFO"))
    logging.basicConfig(level=cfg.get('log_level', "INFO"), format=LOG_FORMAT)