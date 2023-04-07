import asyncio
import json
import logging

from bleak import (
    BleakClient,
    BleakScanner
)

from .commands import (
    DisplayDotMatrixCommand,
    DisplayTextCommand,
    LEDCommand,
    MoveCommand,
    WaitCommand,
    BuzzerCommand
)


class Robot:
    def __init__(self, name, debug=False, scan_timeout=2.0):
        self.name = name
        self.commands = []
        DEBUG = debug
        self.scan_timeout = scan_timeout

        with open("wacrobot/devices_name.json", "r") as f:
            self.device_map = json.load(f)

        if self.name not in self.device_map:
            self.name = name
        else:
            self.name = self.device_map[self.name]

    def led(self, r, g, b, duration: float = 0):
        self.commands.append(LEDCommand(r, g, b))
        self.wait(duration)

    def move(self, right, left, duration: float = 0):
        self.commands.append(MoveCommand(left, right))
        self.wait(duration)

    def stop(self, duration: float = 0):
        self.commands.append(MoveCommand(0, 0))
        self.wait(duration)

    def wait(self, duration: float):
        if duration > 0:
            self.commands.append(WaitCommand(duration))

    def displayText(self, text: str, duration: float = 0):
        self.commands.append(DisplayTextCommand(text))
        self.wait(duration)

    def displayDots(self, matrix: list[int], duration: float = 0):
        self.commands.append(DisplayDotMatrixCommand(matrix))
        self.wait(duration)

    def clearDisplay(self):
        self.commands.append(DisplayDotMatrixCommand())

    def buzz(self, frequency: int, duration: float = 0):
        self.commands.append(BuzzerCommand(frequency))
        self.wait(duration)
        self.commands.append(BuzzerCommand(0))

    async def _execute(self, client):
        logging.debug(client)
        for i, command in enumerate(self.commands):
            logging.debug(f"command {i}/{len(self.commands)}")

            await command.execute(client)

        self.commands = []

    async def _connect_and_run(self):
        scanner = BleakScanner()
        devices = await scanner.discover(timeout=self.scan_timeout, return_adv=False)

        device = None
        for d in devices:
            if d.name == self.name:
                device = d
                break
        
        if device is None:
            raise Exception("Device not found")
        
        logging.debug(f"found device {device.name} at {device.address}")

        async with BleakClient(device.address) as client:
            logging.debug("connected to device")
            await self._execute(client)

    def run(self, clear=True):
        if clear:
            self.commands.append(DisplayDotMatrixCommand())
            self.commands.append(MoveCommand(0, 0))
            self.commands.append(LEDCommand(0, 0, 0))
            self.commands.append(BuzzerCommand(0))
        asyncio.run(self._connect_and_run())
