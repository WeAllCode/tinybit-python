from weallcode_robot import Robot

# Create a robot
name = "dink"
robot = Robot(name)

robot.led(0,0,255,1)

# a = robot.setKeyBinding('a').led(0, 0, 255, 1)
# b = robot.setKeyBinding('b').led(255, 0, 0, 1)
# c = robot.setKeyBinding('c').led(0, 255, 0, 1)

x = robot.setKeyBinding('x')
x.displayText('x')


w = robot.setKeyBinding('w').move(100, 100).displayDots(
    # fmt: off
    [
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 1, 1, 1, 0,
        0, 0, 1, 0, 0,
    ]
)

a = robot.setKeyBinding('a').move(100, 0).displayDots(
    # fmt: off
    [
        0, 0, 0, 0, 0,
        0, 0, 0, 1, 0,
        1, 1, 1, 1, 1,
        0, 0, 0, 1, 0,
        0, 0, 0, 0, 0,
    ]
)

s = robot.setKeyBinding('d').move(0, 100).displayDots(
    # fmt: off
    [
        0, 0, 0, 0, 0,
        0, 1, 0, 0, 0,
        1, 1, 1, 1, 1,
        0, 1, 0, 0, 0,
        0, 0, 0, 0, 0,
    ]
)

d = robot.setKeyBinding('s').move(-100, -100).displayDots(
    # fmt: off
    [
        0, 0, 1, 0, 0,
        0, 1, 1, 1, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
    ]
)