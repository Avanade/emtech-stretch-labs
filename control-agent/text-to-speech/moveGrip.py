import time
import sys

import stretch_body.robot

robot = stretch_body.robot.Robot()
robot.startup()

print("recieved:", sys.argv[1], sys.argv[2])

if sys.argv[1] == "open":
    robot.end_of_arm.move_by("stretch_gripper", float(sys.argv[2]))
elif sys.argv[1] == "close":
    robot.end_of_arm.move_by("stretch_gripper", -1 * float(sys.argv[2]))

robot.push_command()
time.sleep(1)
robot.stop()
