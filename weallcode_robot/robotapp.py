import time
import asyncio
import logging
import atexit
from queue import Queue
from datetime import datetime, timedelta

import sys, os

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.widget import Widget
from textual import events
from textual.reactive import Reactive

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic


class RobotApp(App):

    def init(self):
        self.robot = None