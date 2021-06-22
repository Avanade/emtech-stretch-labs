import time
import sys

import stretch_body.robot

robot = stretch_body.robot.Robot()
robot.startup()
move_by = 0

print("recieved:", sys.argv[1], sys.argv[2])

if sys.argv[1] == "forward":
    move_by = float(sys.argv[2])
elif sys.argv[1] == "backwards":
    move_by = -1 * float(sys.argv[2])


robot.base.translate_by(move_by)
robot.push_command()
time.sleep(5)
robot.stop()
