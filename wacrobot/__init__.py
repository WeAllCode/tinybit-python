__version__ = "0.1.0"
__author__ = "Blaine Rothrock"
__credits__ = "We All Code"

"""
# TODO:
1. Add a license
2. create a flexiBLE JSON Spec for the TinyBit
3. connect to device over BLE
4. send commands to device over BLE
  - Robot("NAME")
5. send a command to change the lights
    - Robot("NAME").led(red, green, blue)
6. send a command to move the robot
    - Robot("NAME").move(wheel1, wheel2, duration)
7. Disconnection handling / stop
"""

DEBUG = False


def print_debug(output):
    if DEBUG:
        print(output)
