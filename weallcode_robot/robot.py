import time
import asyncio
import logging
import atexit
from queue import Queue
from enum import Enum
import tkinter as tk

from bleak import BleakClient, BleakScanner

from .commands import (
    BuzzerCommand,
    DisplayDotMatrixCommand,
    DisplayTextCommand,
    LEDCommand,
    MoveCommand,
    WaitCommand,
)

from .robot_ui import RobotUI

device_name_map = {
    "beep": "WAC-2463",
    "boop": "WAC-7F36",
    "buzz": "WAC-98CE",
    "bzzt": "WAC-D329",
    "chirp": "WAC-1A74",
    "click": "WAC-27B7",
    "clonk": "WAC-9776",
    "clunk": "WAC-7740",
    "crash": "WAC-22F2",
    "dink": "WAC-6BC7",
    "doot": "WAC-47F1",
    "fizz": "WAC-121A",
    "honk": "WAC-5613",
    "hoot": "WAC-9717",
    "jolt": "WAC-A466",
    "noot": "WAC-EC1C",
    "oink": "",
    "pew": "",
    "ping": "",
    "pong": "",
    "pop": "",
    "pow": "",
    "purr": "",
    "quark": "",
    "ring": "",
    "roar": "",
    "sigh": "",
    "snip": "",
    "sput": "",
    "swsh": "",
    "tape": "",
    "thud": "",
    "thum": "",
    "tik": "",
    "tok": "",
    "tong": "",
    "vroom": "",
    "whim": "",
    "whir": "",
    "whiz": "",
    "whoop": "",
    "whum": "",
    "wizz": "",
    "wow": "",
    "yip": "",
    "zap": "",
    "zip": "",
    "zot": "",
}

class RobotState(Enum):
    DISCONNECTED = 0
    CONNECTED_IDLE = 1
    RUNNING = 2
    DONE = 3

class Robot:
    def __init__(self, name, debug=False, scan_timeout=2.0):
        self.display_name = name.lower()
        self.commands = Queue()
        
        self.ui = RobotUI(self)

        self.last_command = Queue()
        
        self.scan_timeout = scan_timeout

        self._update_status('initializing ...', RobotState.DISCONNECTED)

        self.device_map = device_name_map
        self.client = None

        if self.display_name not in self.device_map:
            self.name = self.display_name
        else:
            self.name = self.device_map[self.display_name]
        
        atexit.register(self._run_sync_wrapper)
    
    def led(self, r, g, b, duration: float = 0):
        self.commands.put(LEDCommand(r, g, b))
        self.wait(duration)

    def move(self, right, left, duration: float = 0):
        self.commands.put(MoveCommand(left, right))
        self.wait(duration)

    def stop(self, duration: float = 0):
        self.commands.put(MoveCommand(0, 0))
        self.wait(duration)

    def wait(self, duration: float):
        if duration > 0:
            self.commands.put(WaitCommand(duration))

    def displayText(self, text: str, duration: float = 0):
        self.commands.put(DisplayTextCommand(text))
        self.wait(duration)

    def displayDots(self, matrix: list[int], duration: float = 0):
        self.commands.put(DisplayDotMatrixCommand(matrix))
        self.wait(duration)

    def clearDisplay(self):
        self.commands.put(DisplayDotMatrixCommand())

    def buzz(self, frequency: int, duration: float = 0.25):
        self.commands.put(BuzzerCommand(frequency))
        self.wait(duration)
        self.commands.put(BuzzerCommand(0))

    async def _execute(self, client):
        logging.debug(client)

        self.state = RobotState.RUNNING

        while self.commands.empty() is False:
            command = self.commands.get()
            self._update_status(f"executing {command.__class__.__name__} ...", RobotState.RUNNING)
            await command.execute(client)

        self.state = RobotState.DONE

    
    async def _connect(self):
        scanner = BleakScanner()
        self._update_status('scanning ...', RobotState.DISCONNECTED)
        devices = await scanner.discover(timeout=self.scan_timeout, return_adv=False)

        self._update_status('connecting ...', RobotState.DISCONNECTED)
        device = None
        for d in devices:
            if d.name == self.name:
                device = d
                break

        if device is None:
            self._update_status(f"device {self.name} not found", RobotState.DISCONNECTED)
            raise Exception("Device not found")

        self._update_status(f"found device {device.name} at {device.address}", RobotState.DISCONNECTED)
        logging.debug(f"found device {device.name} at {device.address}")

        self.client = BleakClient(device)
        self._update_status('connecting ...', RobotState.DISCONNECTED)
        await self.client.connect()
        self._update_status('connected', RobotState.CONNECTED_IDLE)

    async def _connect_and_run(self):
        await self._connect()
        if self.client is not None:
            await self._execute(self.client)

    def clear(self):
        self.commands.queue.clear()
        self.commands.put(DisplayDotMatrixCommand())
        self.commands.put(MoveCommand(0, 0))
        self.commands.put(LEDCommand(0, 0, 0))
        self.commands.put(BuzzerCommand(0))
    
    def _run_sync_wrapper(self):
        self.commands.put(DisplayDotMatrixCommand())
        self.commands.put(MoveCommand(0, 0))
        self.commands.put(LEDCommand(0, 0, 0))
        self.commands.put(BuzzerCommand(0))
        
        self.last_command = list(self.commands.queue)
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run())
        loop.close()
    
    async def run(self):
        self.ui.update()
        
        if self.client is None:
            await self._connect()
        
        self.ui.update()

        try:
            while True:
                if self.client is not None:
                    if self.commands.empty():
                        self._update_status('idle', RobotState.CONNECTED_IDLE)
                    else:
                        command = self.commands.get()
                        self._update_status(f"executing {command.__class__.__name__} ...", RobotState.RUNNING)
                        print(f"running command: {command.__class__.__name__}")
                        await command.execute(self.client)
                        
                else:
                    print("no client, waiting ...")
                
                self.ui.update()
        except tk.TclError:
            # cancel current command and clear the robot
            self.clear()
            
            # complete clear on current loop
            if self.client is None: 
                await self._connect_and_run()
            else:
                await self._execute(self.client)
            if self.client is not None:
                await self.client.disconnect()
                self.state = RobotState.DISCONNECTED
            
            print(f"\n{self.name} Done!\n")

    def _update_status(self, msg, state):
        self.status_message = msg
        self.state = state
        self.ui.update()
            
