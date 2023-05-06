__version__ = "3.0.1"

import logging

from .robot import Robot as Robot

logging.basicConfig(
    filename="wac.log",
    encoding="utf-8",
    level=logging.DEBUG,
)
