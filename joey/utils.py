import logging
import sys


def init_logger():
    logformat = "%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s"
    datefmt = "%m-%d %H:%M"

    logging.basicConfig(level=logging.INFO, filemode="w",
                        format=logformat, datefmt=datefmt)
    logger = logging.getLogger("joey")
    return logger