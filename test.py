from wacrobot.robot import Robot

robot = Robot("WAC")

robot.led(255, 0, 0)
robot.move(100, 100)
robot.wait(2)
robot.move(0, 0)
robot.move(-100,100)
robot.wait(0.25)
# robot.move(0, 0)
robot.move(100,100)
robot.wait(1)
robot.move(0,0)
robot.move(-100,-100)
robot.wait(1)
robot.move(0,0)

robot.led(0,0,0)

robot.run()