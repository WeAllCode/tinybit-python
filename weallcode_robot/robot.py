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

        self.buttonA = DynamicObject()
        self.buttonA.led = self.button_a_queue.led
        self.buttonA.move = self.button_a_queue.move
        self.buttonA.stop = self.button_a_queue.stop
        self.buttonA.wait = self.button_a_queue.wait
        self.buttonA.displayText = self.button_a_queue.displayText
        self.buttonA.displayDots = self.button_a_queue.displayDots
        self.buttonA.clearDisplay = self.button_a_queue.clearDisplay
        self.buttonA.buzz = self.button_a_queue.buzz
        self.buttonA.clear = self.button_a_queue.clear

        self.buttonB = DynamicObject()
        self.buttonB.led = self.button_b_queue.led
        self.buttonB.move = self.button_b_queue.move
        self.buttonB.stop = self.button_b_queue.stop
        self.buttonB.wait = self.button_b_queue.wait
        self.buttonB.displayText = self.button_b_queue.displayText
        self.buttonB.displayDots = self.button_b_queue.displayDots
        self.buttonB.clearDisplay = self.button_b_queue.clearDisplay
        self.buttonB.buzz = self.button_b_queue.buzz
        self.buttonB.clear = self.button_b_queue.clear
        
        atexit.register(self.ui.run)
    
    def setKeyBinding(self, key) -> CommandQueue:
        valid_keys = {
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'space', 'enter',
            'up', 'down', 'left', 'right'
        }

        if key not in valid_keys:
            raise ValueError(f"Invalid key {key}, must be in set {valid_keys}")
            
        return self.ui.bind(key)
