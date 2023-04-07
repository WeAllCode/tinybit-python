import threading

from wacrobot.robot import Robot


def run_robot(robot):
    robot.displayText(robot.name, 3)
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
        0.25,
    )
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
    robot.clearDisplay()
    robot.led(255, 0, 0, 0.25)
    robot.led(0, 255, 0, 0.25)
    robot.led(0, 0, 255, 0.25)
    for x in (-100, -80, -60, 60, 80, 100):
        print(x)
        robot.move(x, -x, 0.25)
        robot.stop()
        robot.wait(0.25)
    robot.run()


robots = [
    Robot("chirp"),
    Robot("buzz"),
    Robot("boop"),
    Robot("bzzt"),
    Robot("click"),
]

threads = []
for robot in robots:
    thread = threading.Thread(target=run_robot, args=(robot,))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()
