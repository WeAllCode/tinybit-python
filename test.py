from wacrobot.robot import Robot

# Create a robot named "hoot"
name = "noot"
robot = Robot(name)

# Display "Hi 123!" for 3 seconds
robot.displayText(name.upper(), 2.5)

# Display bullseye for 1 second
robot.displayDots(
    # fmt: off
    [
        1, 1, 1, 1, 1,
        1, 0, 0, 0, 1,
        1, 0, 1, 0, 1,
        1, 0, 0, 0, 1,
        1, 1, 1, 1, 1,
    ],
    # fmt: on
    0.25
)


# Display red bullseye for 1 second
robot.displayDots(
    # fmt: off
    [
        0, 0, 0, 0, 0,
        0, 1, 1, 1, 0,
        0, 1, 0, 1, 0,
        0, 1, 1, 1, 0,
        0, 0, 0, 0, 0,
    ],
    # fmt: on
    0.25,
)

# Clear the display
robot.clearDisplay()

# Display red for 0.5 second
robot.led(255, 0, 0, 0.25)

# Display green for 0.5 second
robot.led(0, 255, 0, 0.25)

# Display blue for 0.5 second
robot.led(0, 0, 255, 0.25)

# Play a tone (Hz) for .5 seconds
robot.buzz(440, 0.25)

# Move 30, 40, 60, 80, 100, -30, -40, -60, -80, -100 percentages for 0.5 seconds
for x in [-100, -80, -60, 60, 80, 100]:
    print(x)
    # Move forward at x% speed for 0.5 seconds
    robot.move(x, -x, 0.25)
    robot.stop()
    robot.wait(0.25)

robot.run()
