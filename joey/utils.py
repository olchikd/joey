import logging
import sys


def init_logger():
    logformat = "%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s"
    datefmt = "%m-%d %H:%M"

    logging.basicConfig(level=logging.INFO, filemode="w",
                        format=logformat, datefmt=datefmt)

    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(logging.Formatter(fmt=logformat, datefmt=datefmt))

    logger = logging.getLogger("joye")
    logger.addHandler(stream_handler)
    return logger