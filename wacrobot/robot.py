import asyncio
import json

from bleak import BleakClient

from . import DEBUG, print_debug
from .commands import (
    DisplayDotMatrixCommand,
    DisplayTextCommand,
    LEDCommand,
    MoveCommand,
    WaitCommand,
)


class Robot:
    def __init__(self, name, debug=False):
        self.name = name
        self.commands = []
        DEBUG = debug

        with open("wacrobot/devices.json", "r") as f:
            self.device_map = json.load(f)

        if self.name not in self.device_map:
            self.address = name
        else:
            self.address = self.device_map[self.name]

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

    async def _execute(self, client: BleakClient):
        print_debug(client)

        for i, command in enumerate(self.commands):
            print_debug(f"command {i}/{len(self.commands)}")

            await command.execute(client)

        self.commands = []

    async def _connect_and_run(self):
        async with BleakClient(self.address) as client:
            print_debug("connected to device")
            await self._execute(client)

    def run(self, clear=True):
        if clear:
            self.commands.append(DisplayDotMatrixCommand())
            self.commands.append(MoveCommand(0, 0))
            self.commands.append(LEDCommand(0, 0, 0))
        asyncio.run(self._connect_and_run())
