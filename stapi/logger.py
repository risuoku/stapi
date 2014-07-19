import logging
from stapi.config import Config
from stapi.error import StError

class Logger(object):
  def __init__(self):
    conf = Config.load_log()

    # log format setting
    FORMAT = conf['format']

    # log level setting
    if conf['level'] == "debug":
      LEVEL = logging.DEBUG
    elif conf['level'] == "info":
      LEVEL = logging.INFO
    elif conf['level'] == "warn":
      LEVEL = logging.WARNING
    elif conf['level'] == "error":
      LEVEL = logging.ERROR
    elif conf['level'] == "crit":
      LEVEL = logging.CRITICAL
    else:
      raise StError("incorrect log level setting")

    if not conf['filename'] == "stdout":
      FILENAME = conf['filename']
      logging.basicConfig(
        level = LEVEL, format=FORMAT, filename=FILENAME
      )
    else:
      logging.basicConfig(
        level = LEVEL, format=FORMAT
      )

  def debug(self, msg):
    logging.debug(msg)

  def info(self, msg):
    logging.info(msg)

  def warn(self, msg):
    logging.warning(msg)

  def error(self, msg):
    logging.error(msg)

  def crit(self, msg):
    logging.critical(msg)
