from datetime import datetime

from wacrobot.robot import Robot

robot = Robot("boop")

while True:
    robot.move(-100, 100)
    robot.led(255, 255, 255)
    robot.wait(1)

    # print date and time
    print(datetime.now().strftime("%H:%M:%S"))

    robot.run(False)
