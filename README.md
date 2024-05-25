# Micro:bit TinyBit BLE Python Library

A Python package to control a custom Robot V2 via Bluetooth Low Energy (BLE) communication. The package provides an API for controlling the robot's movements and LED colors.

## Installation

This project uses [Poetry](https://python-poetry.org/) for package management. Install Poetry if you haven't already.

To install the package and its dependencies, run:

```bash
poetry install
```

## Usage

The `example.py` script demonstrates how to use the package to control the robot.

```python
from weallcode_robot import Robot

robot = Robot("WAC")

robot.led(255, 0, 0)        # Set the LED color to red
robot.move(100, 100)        # Move forward
robot.wait(2)               # Wait for 2 seconds
robot.move(0, 0)            # Stop the robot
robot.move(-100, 100)       # Turn the robot
robot.wait(0.25)            # Wait for 0.25 seconds
robot.move(100, 100)        # Move forward
robot.wait(1)               # Wait for 1 second
robot.move(0, 0)            # Stop the robot
robot.move(-100, -100)      # Move backward
robot.wait(1)               # Wait for 1 second
robot.move(0, 0)            # Stop the robot

robot.led(0, 0, 0)          # Turn off the LED

a = robot.setKeyBinding('a').led(0, 0, 255, 1) # set LED color one button A
w = robot.setKeyBinding('w').move(100, 100)    # bind move forward to key W
```

## API

### Robot

The `Robot` class is the main class to control the robot. Instantiate the class with the name of the robot.

```python
robot = Robot("WAC")
```

#### Methods

- `led(red: int, green: int, blue: int, duration: int)`: Sets the LED color. Values should be integers between 0 and 255.
- `move(left: int, right: int, duration: int)`: Sets the motor speeds. Values should be integers between -100 and 100.
- `wait(duration: float)`: Adds a wait command with a given duration in seconds.
- `run()`: Executes the commands in the order they were added.

## Development

The package includes development dependencies:

- `black`: Code formatter
- `pre-commit`: Pre-commit hooks for code formatting and linting
- `isort`: Import sorter
- `ruff`: Linter

To install the development dependencies, run:

```bash
poetry install --extras dev
```

To run the pre-commit hooks, first install them:

```bash
pre-commit install
```

Then run:

```bash
pre-commit run --all-files
```

## Authors

- Blaine Rothrock
- Ali Karbassi
