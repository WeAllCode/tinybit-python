from wacrobot.robot import Robot

robot = Robot("wac-dev01")

robot.displayText("Woooooooo!")
robot.wait(1)
robot.led(100, 0, 0)
robot.move(100,100)
robot.wait(0.5)
robot.move(-60,60)
robot.wait(0.22)
robot.move(100,100)
robot.wait(0.5)
robot.stop()
robot.displayDots([1,1,1,1,1,
                   1,0,0,0,1,
                   1,0,0,0,1,
                   1,0,0,0,1,
                   1,1,1,1,1])
robot.wait(3)
robot.clearDisplay()

robot.run()
