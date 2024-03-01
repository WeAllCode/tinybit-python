import time
import asyncio
import logging
import atexit
from queue import Queue
import tkinter as tk
from datetime import datetime, timedelta

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

from .commands import (
    CommandQueue,
    BuzzerCommand,
    DisplayDotMatrixCommand,
    DisplayTextCommand,
    LEDCommand,
    MoveCommand,
    WaitCommand,
)

from .robot_ui import RobotUI
from .utils import (
    RobotState, 
    DynamicObject,
    device_name_map, 
    buttons_characteristic_uuid
)

class Robot(CommandQueue):
    def __init__(self, name, debug=False):
        
        self.display_name = name.lower()
        if self.display_name not in device_name_map:
            self.name = self.display_name
        else:
            self.name = device_name_map[self.display_name]

        self.ui = RobotUI(robot=self)
        
        self.command_tasks = None
        self.last_key_event = datetime.now()
        
        self.main_queue = CommandQueue(f'{self.display_name} main')
        self.button_a_queue = CommandQueue(f'{self.display_name} button a')
        self.button_b_queue = CommandQueue(f'{self.display_name} button b')
        self.commands = self.main_queue

        # map commands
        self.led = self.main_queue.led
        self.move = self.main_queue.move
        self.stop = self.main_queue.stop
        self.wait = self.main_queue.wait
        self.displayText = self.main_queue.displayText
        self.displayDots = self.main_queue.displayDots
        self.clearDisplay = self.main_queue.clearDisplay
        self.buzz = self.main_queue.buzz
        self.clear = self.main_queue.clear

        self.button_a = DynamicObject()
        self.button_a.led = self.button_a_queue.led
        self.button_a.move = self.button_a_queue.move
        self.button_a.stop = self.button_a_queue.stop
        self.button_a.wait = self.button_a_queue.wait
        self.button_a.displayText = self.button_a_queue.displayText
        self.button_a.displayDots = self.button_a_queue.displayDots
        self.button_a.clearDisplay = self.button_a_queue.clearDisplay
        self.button_a.buzz = self.button_a_queue.buzz
        self.button_a.clear = self.button_a_queue.clear

        self.button_b = DynamicObject()
        self.button_b.led = self.button_b_queue.led
        self.button_b.move = self.button_b_queue.move
        self.button_b.stop = self.button_b_queue.stop
        self.button_b.wait = self.button_b_queue.wait
        self.button_b.displayText = self.button_b_queue.displayText
        self.button_b.displayDots = self.button_b_queue.displayDots
        self.button_b.clearDisplay = self.button_b_queue.clearDisplay
        self.button_b.buzz = self.button_b_queue.buzz
        self.button_b.clear = self.button_b_queue.clear
        
        atexit.register(self.ui.run)
    
    def set_key_binding(self, key) -> CommandQueue:
        valid_keys = {
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'space', 'enter',
            'up', 'down', 'left', 'right'
        }

        if key not in valid_keys:
            raise ValueError(f"Invalid key {key}, must be in set {valid_keys}")
            
        return self.ui.bind(key)
