import asyncio
import time
import json
from datetime import datetime, timedelta
from .commands import RobotCommandType, RobotCommand, LEDCommand, MoveCommand, WaitCommand
from bleak import BleakClient, BleakScanner

class Robot:
    def __init__(self, name):
        self.name = name
        self.led_service_uuid = "1A230001-C2ED-4D11-AD1E-FC06D8A02D37".lower()
        self.led_char_uuid = "1A230002-C2ED-4D11-AD1E-FC06D8A02D37".lower()
        self.wheel_service_uuid = "1A240001-C2ED-4D11-AD1E-FC06D8A02D37".lower()
        self.wheel_char_uuid = "1A240002-C2ED-4D11-AD1E-FC06D8A02D37".lower()
        self.commands = []

        with open('wacrobot/devices.json', 'r') as f:
            self.device_map = json.load(f)

        if self.name not in self.device_map:
            self.address = name
        else: 
            self.address = self.device_map[self.name]

    def led(self, r, g, b):
        self.commands.append(LEDCommand(r, g, b))

    def move(self, right, left):
        self.commands.append(MoveCommand(left, right))

    def wait(self, duration):
        self.commands.append(WaitCommand(duration))

    async def _execute(self, client):
        print(client)
        for i, command in enumerate(self.commands):
            print(f'command {i}/{len(self.commands)}')
            await command.execute(client)

    async def _connect_and_run(self):
        scanner = BleakScanner()

        async with BleakClient(self.address) as client:
            print("connected to device")
            await self._execute(client)

    def run(self):
        self.commands.append(MoveCommand(0,0))
        self.commands.append(LEDCommand(0,0,0))
        asyncio.run(self._connect_and_run())
