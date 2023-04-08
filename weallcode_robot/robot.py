import asyncio
import json
import logging

from bleak import BleakClient, BleakScanner

from .commands import (
    BuzzerCommand,
    DisplayDotMatrixCommand,
    DisplayTextCommand,
    LEDCommand,
    MoveCommand,
    WaitCommand,
)

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
  "zot": ""
}

class Robot:
    def __init__(self, name, debug=False, scan_timeout=2.0):
        self.name = name.lower()
        self.commands = []
        self.scan_timeout = scan_timeout

        self.device_map = device_name_map

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
