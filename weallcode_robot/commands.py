import asyncio
import logging
from queue import Queue

from bleak import BleakClient

from .utils import copy_asyncio_queue, empty_asyncio_queue


class CommandQueue():
    def __init__(self, name: str):
        self.name = name
        
        self.queue = asyncio.Queue(maxsize=100)
        self._queue = None

    def put(self, command):
        if not self.queue.full():
            self.queue.put_nowait(command)

    async def get(self):
        return await self.queue.get()
    
    def empty(self):
        return self.queue.empty()
    
    def led(self, red, green, blue, duration: float = 0):
        self.put(LEDCommand(red, green, blue))
        self.wait(duration)
        return self

    def move(self, left, right, duration: float = 0):
        self.put(MoveCommand(left, right))
        self.wait(duration)
        return self

    def stop(self, duration: float = 0):
        self.put(MoveCommand(0, 0))
        self.wait(duration)
        return self

    def wait(self, duration: float):
        if duration > 0:
            self.put(WaitCommand(duration))
        return self

    def displayText(self, text: str, duration: float = 0):
        self.put(DisplayTextCommand(text))
        self.wait(duration)
        return self

    def displayDots(self, matrix: list[int], duration: float = 0):
        self.put(DisplayDotMatrixCommand(matrix))
        self.wait(duration)
        return self

    def clearDisplay(self):
        self.put(DisplayDotMatrixCommand())
        return self

    def buzz(self, frequency: int, duration: float = 0.25):
        self.put(BuzzerCommand(frequency))
        self.wait(duration)
        return self

    async def clear_immediate(self):
        await empty_asyncio_queue(self.queue)
        self.clear()
        return self
    
    def clear(self):
        self.put(DisplayDotMatrixCommand())
        self.put(MoveCommand(0, 0))
        self.put(LEDCommand(0, 0, 0))
        self.put(BuzzerCommand(0))
        return self

    async def save(self):
        self._queue = await copy_asyncio_queue(self.queue)

    def save_sync(self):
        self._queue = self.queue

    async def restore(self):
        if self._queue:
            self.queue = await copy_asyncio_queue(self._queue)

    def restore_sync(self):
        if self._queue:
            self.queue = self._queue

class RobotCommand:
    def __init__(self):
        pass

    def __str__(self):
        return f"RobotCommand: {self.command_type}"

    def command() -> bytes:
        pass

    async def execute(self, client: BleakClient):
        pass


class LEDCommand(RobotCommand):
    def __init__(self, red: int, green: int, blue: int):
        super().__init__()

        self._service_uuid = "1A230001-C2ED-4D11-AD1E-FC06D8A02D37"
        self._char_uuid = "1A230002-C2ED-4D11-AD1E-FC06D8A02D37"

        # limit between 0 - 255
        self.red = min(255, max(0, red))
        self.green = min(255, max(0, green))
        self.blue = min(255, max(0, blue))

    def command(self):
        return bytes([self.red, self.green, self.blue])

    async def execute(self, client: BleakClient):
        logging.debug(f"led command: {self.command()}")
        service = client.services.get_service(self._service_uuid)
        char = service.get_characteristic(self._char_uuid)

        logging.debug(f"led service: {service}, config char: {char}")

        await client.write_gatt_char(char, self.command(), response=True)
        logging.debug("sent led command")


class MoveCommand(RobotCommand):
    def __init__(self, left: int, right: int):
        super().__init__()

        self._service_uuid = "1A240001-C2ED-4D11-AD1E-FC06D8A02D37"
        self._char_uuid = "1A240002-C2ED-4D11-AD1E-FC06D8A02D37"

        left = min(100, max(-100, left))
        right = min(100, max(-100, right))

        self.left_fwd = left if left > 0 else 0
        self.left_rev = -left if left < 0 else 0
        self.right_fwd = right if right > 0 else 0
        self.right_rev = -right if right < 0 else 0

    def command(self):
        return bytes([self.left_fwd, self.left_rev, self.right_fwd, self.right_rev])

    async def execute(self, client: BleakClient):
        logging.debug(f"wheels command: {self.command()}")
        service = client.services.get_service(self._service_uuid)
        char = service.get_characteristic(self._char_uuid)

        await client.write_gatt_char(char, self.command(), response=True)
        logging.debug("sent wheels command")


class DisplayTextCommand(RobotCommand):
    def __init__(self, text: str):
        super().__init__()

        self._service_uuid = "1A250001-C2ED-4D11-AD1E-FC06D8A02D37"
        self._char_uuid = "1A250002-C2ED-4D11-AD1E-FC06D8A02D37"

        self.text = text

    def command(self):
        return bytes([0x01] + list(self.text.encode("ascii")))

    async def execute(self, client: BleakClient):
        logging.debug(f"display text command: {self.text} (command: {self.command()})")
        service = client.services.get_service(self._service_uuid)
        char = service.get_characteristic(self._char_uuid)

        await client.write_gatt_char(char, self.command(), response=True)
        logging.debug("sent display text command")


class DisplayDotMatrixCommand(RobotCommand):
    def __init__(self, matrix: list[int] = [0] * 25):
        super().__init__()

        self._service_uuid = "1A250001-C2ED-4D11-AD1E-FC06D8A02D37"
        self._char_uuid = "1A250002-C2ED-4D11-AD1E-FC06D8A02D37"

        self.matrix = matrix

    def command(self):
        return bytes([0x02] + self.matrix)

    async def execute(self, client: BleakClient):
        logging.debug(
            f"display text command: {self.matrix} (command: {self.command()})"
        )
        service = client.services.get_service(self._service_uuid)
        char = service.get_characteristic(self._char_uuid)

        await client.write_gatt_char(char, self.command(), response=True)
        logging.debug("sent display text command")


class BuzzerCommand(RobotCommand):
    def __init__(self, frequency: int):
        super().__init__()

        self._service_uuid = "1A260001-C2ED-4D11-AD1E-FC06D8A02D37"
        self._char_uuid = "1A260002-C2ED-4D11-AD1E-FC06D8A02D37"

        self.frequency = frequency

    def command(self):
        return self.frequency.to_bytes(2, "big")

    async def execute(self, client: BleakClient):
        logging.debug(f"buzzer command: {self.frequency}Hz, ({self.command()})")
        service = client.services.get_service(self._service_uuid)
        char = service.get_characteristic(self._char_uuid)

        await client.write_gatt_char(char, self.command(), response=True)
        logging.debug("sent buzzer command")


class WaitCommand(RobotCommand):
    def __init__(self, duration: float):
        super().__init__()
        self.duration = duration

    def command(self):
        return bytes()

    async def execute(self, client: BleakClient):
        await asyncio.sleep(self.duration)
