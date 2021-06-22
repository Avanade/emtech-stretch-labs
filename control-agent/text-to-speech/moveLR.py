import time
import sys

import stretch_body.robot

robot = stretch_body.robot.Robot()
robot.startup()
rotate_by = 0

print("recieved:", sys.argv[1], sys.argv[2])

if sys.argv[1] == "left":
    rotate_by = float(sys.argv[2])
elif sys.argv[1] == "right":
    rotate_by = -1 * float(sys.argv[2])

if sys.argv[1] == "right" or "left":
    robot.base.rotate_by(rotate_by)
    robot.push_command()

time.sleep(2)
robot.stop()
