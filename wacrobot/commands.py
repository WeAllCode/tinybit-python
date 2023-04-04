from enum import Enum
import asyncio

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

WHEELS_SERVICE_UUID: str = '1A240001-C2ED-4D11-AD1E-FC06D8A02D37'
WHEELS_CONFIG_CHAR_UUID: str = '1A240002-C2ED-4D11-AD1E-FC06D8A02D37'

class RobotCommandType(Enum):
    LED = 1
    MOVE = 2
    STOP = 3
    WAIT = 4

class RobotCommand:
    def __init__(self, command_type: RobotCommandType):
        self.command_type = command_type

    def __str__(self):
        return f'RobotCommand: {self.command_type}'
    
    def command() -> bytes:
        pass

    async def execute(self, client: BleakClient):
        pass

class LEDCommand(RobotCommand):
    def __init__(self, red: int, green: int, blue: int):
        super().__init__(RobotCommandType.LED)

        self._service_uuid = '1A230001-C2ED-4D11-AD1E-FC06D8A02D37'
        self._char_uuid = '1A230002-C2ED-4D11-AD1E-FC06D8A02D37'
        
        # limit between 0 - 255
        self.red = min(255, max(0, red))
        self.green = min(255, max(0, green))
        self.blue = min(255, max(0, blue))

    def command(self):
        return bytes([self.red, self.green, self.blue])
    
    async def execute(self, client: BleakClient):
        print(f'led command: {self.command()}')
        
        service = client.services.get_service(self._service_uuid)
        char = service.get_characteristic(self._char_uuid) 

        print(f'led service: {service}, config char: {char}')

        await client.write_gatt_char(char, self.command(), response=True)
        print('sent led command')


class MoveCommand(RobotCommand):
    def __init__(self, left: int, right: int):
        super().__init__(RobotCommandType.MOVE)
        
        left = min(100, max(-100, left))
        right = min(100, max(-100, right))
        
        self.left_fwd = left if left > 0 else 0
        self.left_rev = -left if left < 0 else 0
        self.right_fwd = right if right > 0 else 0
        self.right_rev = -right if right < 0 else 0

    def command(self):
        return bytes([self.left_fwd, self.left_rev, self.right_fwd, self.right_rev])
    
    async def execute(self, client: BleakClient):
        print(f'wheels command: {self.command()}')
        service = client.services.get_service(WHEELS_SERVICE_UUID)
        char = service.get_characteristic(WHEELS_CONFIG_CHAR_UUID) 

        await client.write_gatt_char(char, self.command(), response=True)
        print('sent wheels command')


class WaitCommand(RobotCommand):
    def __init__(self, duration: int):
        super().__init__(RobotCommandType.WAIT)
        self.duration = duration

    def command(self):
        return bytes()
    
    async def execute(self, client: BleakClient):
        await asyncio.sleep(self.duration)