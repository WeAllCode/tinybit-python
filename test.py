from wacrobot.robot import Robot

robot = Robot("wac-dev01")

robot.led(100, 0, 0)
robot.move(100,100)
robot.wait(0.5)
robot.move(-60,60)
robot.wait(0.1)
robot.move(100,100)
robot.wait(0.5)

robot.run()
