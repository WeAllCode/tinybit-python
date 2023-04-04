import asyncio

from bleak import BleakClient, BleakScanner


class Robot:
    def __init__(self, name):
        self.name = name
        self.led_service_uuid = "1A230001-C2ED-4D11-AD1E-FC06D8A02D37".lower()
        self.led_char_uuid = "1A230002-C2ED-4D11-AD1E-FC06D8A02D37".lower()
        self.wheel_service_uuid = "1A240001-C2ED-4D11-AD1E-FC06D8A02D37".lower()
        self.wheel_char_uuid = "1A240002-C2ED-4D11-AD1E-FC06D8A02D37".lower()
        self.commands = []

    def led(self, r, g, b):
        self.commands.append(("led", r, g, b))

    def move(self, right, left):
        self.commands.append(("move", right, left))

    def wait(self, duration):
        self.commands.append(("wait", duration))

    async def _execute(self, client):
        print(client)
        for command in self.commands:
            if command[0] == "led":
                service = client.services.get_service(self.led_service_uuid)
                char = service.get_characteristic(self.led_char_uuid)

                r, g, b = command[1], command[2], command[3]
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))

                bytes = bytearray([r, g, b])

                await client.write_gatt_char(char, bytes, response=True)
                print(f"send led command {bytes} {char}")
            elif command[0] == "move":
                service = client.services.get_service(self.wheel_service_uuid)
                char = service.get_characteristic(self.wheel_char_uuid)

                right, left = command[1], command[2]
                right = max(-100, min(100, right))
                left = max(-100, min(100, left))
                right_forward = max(0, right)
                right_backward = max(0, -right)
                left_forward = max(0, left)
                left_backward = max(0, -left)

                bytes = bytearray(
                    [right_forward, right_backward, left_forward, left_backward]
                )
                await client.write_gatt_char(char, bytes, response=True)
                print(f"send move command {bytes} {char}")
            elif command[0] == "wait":
                duration = command[1]
                await asyncio.sleep(duration)

    async def _connect_and_run(self):
        scanner = BleakScanner()
        devices = await scanner.discover()

        device_address = None
        for device in devices:
            if device.name == self.name:
                device_address = device.address
                break

        if device_address is None:
            raise ValueError(f"Device with name {self.name} was not found")

        print(f"{self.name} found at {device_address}")

        async with BleakClient(device_address) as client:
            print("connected to device")
            await self._execute(client)

    def run(self):
        asyncio.run(self._connect_and_run())
