import time
import sys

import stretch_body.robot

robot = stretch_body.robot.Robot()
robot.startup()
move_by = 0

forward_back = sys.argv[1]
ammount = sys.argv[2]

if forward_back == "forward":
    move_by = float(ammount)
elif forward_back == "backwards":
    move_by = -1 * float(ammount)


robot.base.translate_by(move_by)
robot.push_command()
time.sleep(5)
robot.stop()
