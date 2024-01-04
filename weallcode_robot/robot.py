import time
import asyncio
import logging
import atexit
from queue import Queue
import tkinter as tk

from bleak import BleakClient, BleakScanner

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
from .utils import RobotState, device_name_map

class Robot(CommandQueue):
    def __init__(self, name, debug=False, scan_timeout=2.0):
        
        self.display_name = name.lower()
        if self.display_name not in device_name_map:
            self.name = self.display_name
        else:
            self.name = device_name_map[self.display_name]
        
        self.scan_timeout = scan_timeout
        self.client = None
        
        self.ui = RobotUI(self)
        
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
        
        self._update_status('initializing ...', RobotState.DISCONNECTED)
        
        atexit.register(self._run_sync_wrapper)

    async def _execute(self, client):
        logging.debug(client)

        self._update_status('running ...', RobotState.RUNNING)

        while self.commands.empty() is False:
            command = await self.commands.get()
            self._update_status(f"executing {command.__class__.__name__} ...", RobotState.RUNNING)
            await command.execute(client)

        self._update_status('idle', RobotState.CONNECTED_IDLE)

    
    async def _connect(self):
        scanner = BleakScanner()
        self._update_status('scanning ...', RobotState.CONNECTING)
        devices = await scanner.discover(timeout=self.scan_timeout, return_adv=False)

        self._update_status('connecting ...', RobotState.CONNECTING)
        device = None
        for d in devices:
            if d.name == self.name:
                device = d
                break

        if device is None:
            self._update_status(f"device {self.name} not found", RobotState.DISCONNECTED)
            raise Exception("Device not found")

        self._update_status(f"found device {device.name} at {device.address}", RobotState.CONNECTING)
        logging.debug(f"found device {device.name} at {device.address}")

        self.client = BleakClient(device)
        self._update_status('connecting ...', RobotState.CONNECTING)
        await self.client.connect()
        self._update_status('connected', RobotState.CONNECTED_IDLE)

    async def _connect_and_run(self):
        await self._connect()
        if self.client is not None:
            await self._execute(self.client)

    def clear(self):
        self.commands.clear(immediate=True)
    
    def _run_sync_wrapper(self):                        
        loop = asyncio.get_event_loop()
        
        try:
            loop.run_until_complete(self.commands.clear())
            loop.run_until_complete(self.commands.save())
            t1 = loop.create_task(self._ui_loop())
            t2 = loop.create_task(self.run())

            loop.run_until_complete(asyncio.gather(t1, t2))
        
        except tk.TclError:
            # cancel current command and clear the robot
            self.clear()
            
            # complete clear on current loop
            if self.client is None: 
                loop.run_until_complete(self._connect_and_run())
            else:
                loop.run_until_complete(self._execute(self.client))
            
            if self.client is not None:
                loop.run_until_complete(self.client.disconnect())
                self._update_status('disconnected', RobotState.DISCONNECTED)
            
            print(f"\n{self.name} Done!\n") 
        
        finally:
            loop.close()
    
    async def _ui_loop(self):
        while True:
            self.ui.update()
            await asyncio.sleep(0.1)
    
    async def run(self):        
        if self.client is None:
            await self._connect()

        while True:
            if self.client is not None:
                if self.commands.empty():
                    self._update_status('idle', RobotState.CONNECTED_IDLE)
                    await asyncio.sleep(0.1)
                else:
                    command = await self.commands.get()
                    self._update_status(f"executing {command.__class__.__name__} ...", RobotState.RUNNING)
                    print(f"running command: {command.__class__.__name__}")
                    await command.execute(self.client)
                    
            else:
                self._update_status('disconnected', RobotState.DISCONNECTED)

    def _update_status(self, msg, state):
        self.status_message = msg
        self.state = state
            
