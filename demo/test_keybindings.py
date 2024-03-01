from weallcode_robot import Robot

# Create a robot
name = "WAC-C9B9"
robot = Robot(name)

robot.led(0,0,255,1)

a = robot.set_key_binding('a').led(0, 0, 255, 1)
b = robot.set_key_binding('b').led(255, 0, 0, 1)
c = robot.set_key_binding('c').led(0, 255, 0, 1)

w = robot.set_key_binding('w').move(100, 100).displayDots(
    # fmt: off
    [
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 1, 1, 1, 0,
        0, 0, 1, 0, 0,
    ]
)
a = robot.set_key_binding('a').move(100, 0).displayDots(
    # fmt: off
    [
        0, 0, 0, 0, 0,
        0, 0, 0, 1, 0,
        1, 1, 1, 1, 1,
        0, 0, 0, 1, 0,
        0, 0, 0, 0, 0,
    ]
)
s = robot.set_key_binding('d').move(0, 100).displayDots(
    # fmt: off
    [
        0, 0, 0, 0, 0,
        0, 1, 0, 0, 0,
        1, 1, 1, 1, 1,
        0, 1, 0, 0, 0,
        0, 0, 0, 0, 0,
    ]
)
d = robot.set_key_binding('s').move(-100, -100).displayDots(
    # fmt: off
    [
        0, 0, 1, 0, 0,
        0, 1, 1, 1, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
    ]
)