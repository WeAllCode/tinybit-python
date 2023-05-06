__version__ = "3.0.1"
__author__ = "Blaine Rothrock"
__credits__ = "We All Code"

import logging

from .robot import Robot as Robot

logging.basicConfig(
    filename="wac.log",
    encoding="utf-8",
    level=logging.DEBUG,
)
