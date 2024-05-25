import copy

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.widget import Widget
from textual import events, work
from textual.reactive import reactive

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

from .utils import (
    RobotState, 
    DynamicObject,
    device_name_map, 
    buttons_characteristic_uuid
)

from .commands import (
    CommandQueue,
    BuzzerCommand,
    DisplayDotMatrixCommand,
    DisplayTextCommand,
    LEDCommand,
    MoveCommand,
    WaitCommand,
)

from .commands import *
from .utils import RobotState


class RobotStatus(Widget):
    """A widget to display elapsed time."""

    status = reactive("idle")

    def render(self) -> str:
        return f"Status: {self.status}"


class RobotUI(App):
    BINDINGS = [
        ("escape", "quit", "Quit Application")
    ]

    def __init__(self, robot, **kwargs):
        super().__init__(**kwargs)
        self.robot = robot
        self.running = 0
        
        self.key_commands = {}

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(name=f"WeAllCode: {self.robot.display_name}")
        yield Footer()
        yield RobotStatus()

    def on_mount(self) -> None:
        self.run_worker(self._connect_and_run())

    def on_key(self, event: events.Key) -> None:
        if event.key in self.key_commands:
            self.update_status(f"running key {event.key} ...")
            commands = copy.deepcopy(self.key_commands[event.key]).clear().clearDisplay()
            self.run_worker(self.execute(commands))


    def execute(self, command):
        self.run_worker(command)

    def action_quit(self) -> None:
        self.exit()

    def update_status(self, status):
        self.query_one(RobotStatus).status = status

    def bind(self, key) -> CommandQueue:
        self.key_commands[key] = CommandQueue(f'{self.robot.display_name}-{key}')
        return self.key_commands[key]

    async def _connect_and_run(self):
        self.update_status(f'scanning for {self.robot.display_name} ...')
        device = await BleakScanner.find_device_by_name(self.robot.name, timeout=10.0)

        self.update_status(f'connecting to {self.robot.display_name} ...')

        if device is None:
            self.update_status(f"device {self.robot.name} not found. Quit and try again.")
            return

        self.update_status(f"found device {device.name} at {device.address}")
        logging.debug(f"found device {device.name} at {device.address}")

        self.client = BleakClient(device)
        self.update_status('connecting ...')
        await self.client.connect()

        def _button_handler_callback(characteristic: BleakGATTCharacteristic, data: bytearray):
            btn = int(data[0])
            if btn == 1:
                self.update_status('running button a ...')
                if self.robot.button_a_queue.empty():
                    commands = CommandQueue(f'{self.robot.display_name} button a').displayText("A", 1).clear().clearDisplay()
                else:
                    commands = copy.deepcopy(self.robot.button_a_queue).clear().clearDisplay()
                self.run_worker(self.execute(commands))
            elif btn == 2:
                self.update_status('running button a ...')
                if self.robot.button_b_queue.empty():
                    commands = CommandQueue(f'{self.robot.display_name} button b').displayText("B", 1).clear().clearDisplay()
                else:
                    commands = copy.deepcopy(self.robot.button_b_queue).clear().clearDisplay()
                self.run_worker(self.execute(commands))

        await self.client.start_notify(buttons_characteristic_uuid, _button_handler_callback)
        self.update_status('connected')

        self.update_status('running ...')

        commands = copy.deepcopy(self.robot.commands).clear().clearDisplay()

        await self.execute(commands)

        if self.robot.button_a_queue.empty() and self.robot.button_b_queue.empty() and not self.key_commands:
            self.exit()

    async def execute(self, commands):     
        if self.running == 1: return

        self.running = 1
        while commands.empty() is False:
            command = await commands.get()
            # self.update_status(f"executing {command.__class__.__name__} ...")
            await command.execute(self.client)

        if not self.key_commands and self.robot.button_a_queue.empty() and self.robot.button_b_queue.empty():
            return
        else:
            self.update_status('idle')
            self.running = 0

    async def clear(self):
        self.running = 1

        commands = CommandQueue(f'{self.robot.display_name}-{key}').clear().clearDisplay()
        while commands.empty() is False:
            command = await commands.get()
            await command.execute(self.client)

        self.update_status('idle')
        self.running = 0