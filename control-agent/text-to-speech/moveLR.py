import time
import sys

import stretch_body.robot

robot = stretch_body.robot.Robot()
robot.startup()
rotate_by = 0

left_right = sys.argv[1]
ammount = sys.argv[2]

print("recieved:", left_right, ammount)

if left_right == "left":
    rotate_by = float(ammount)
elif left_right == "right":
    rotate_by = -1 * float(ammount)

if left_right == "right" or "left":
    robot.base.rotate_by(rotate_by)
    robot.push_command()

time.sleep(2)
robot.stop()
