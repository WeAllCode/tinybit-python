__version__ = "0.1.0"
__author__ = "Blaine Rothrock"
__credits__ = "We All Code"

import logging
from .robot import Robot

logging.basicConfig(
    filename="wac.log",
    encoding="utf-8",
    level=logging.DEBUG,
)
