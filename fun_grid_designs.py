from wacrobot.robot import Robot


def draw_progressBar(robot: Robot, duration=0.5):
    for i in range(26):
        robot.displayDots([1] * i + [0] * (25 - i), duration)


def draw_rows(robot: Robot, duration=0.25):
    # Turn on each row one at a time
    for i in range(-1, 5, 1):
        dots = [1 if j // 5 == i else 0 for j in range(25)]
        robot.displayDots(dots, duration)

    # Turn off each row one at a time
    for i in range(3, -1, -1):
        dots = [1 if j // 5 == i else 0 for j in range(25)]
        robot.displayDots(dots, duration)

    robot.clearDisplay()


def draw_led_grid(robot: Robot, duration=0.25):
    led_grid = [[0] * 5 for _ in range(5)]
    for i in range(5):
        for j in range(i + 1):
            led_grid[i][j] = 1
            led_grid[j][i] = 1
        robot.displayDots([led for row in led_grid for led in row], duration)
        robot.wait(duration)

    robot.clearDisplay()


def draw_hollow_square(robot: Robot):
    led_grid = [[0] * 5 for _ in range(5)]
    for i in range(5):
        led_grid[i][0] = 1
        led_grid[i][4] = 1
        led_grid[0][i] = 1
        led_grid[4][i] = 1
    robot.displayDots([led for row in led_grid for led in row])


def draw_house(robot: Robot):
    led_grid = [[0] * 5 for _ in range(5)]
    for j in range(3):
        led_grid[4][j + 1] = 1
    for i in range(4):
        for j in range(i + 1):
            led_grid[i][2 - j : 3 + j] = [1] * (2 * j + 1)

    robot.displayDots([led for row in led_grid for led in row])


def draw_x(robot: Robot):
    led_grid = [[0] * 5 for _ in range(5)]
    for i in range(5):
        led_grid[i][i] = 1
        led_grid[i][4 - i] = 1
    robot.displayDots([led for row in led_grid for led in row])
