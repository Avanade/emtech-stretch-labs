import time
import sys

import stretch_body.robot

robot = stretch_body.robot.Robot()
robot.startup()

open_close = sys.argv[1]
ammount = sys.argv[2]

if open_close == "open":
    robot.end_of_arm.move_by("stretch_gripper", float(ammount))
elif open_close == "close":
    robot.end_of_arm.move_by("stretch_gripper", -1 * float(ammount))

robot.push_command()
time.sleep(1)
robot.stop()
