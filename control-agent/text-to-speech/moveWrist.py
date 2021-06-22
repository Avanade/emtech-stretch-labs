import time
import sys

import stretch_body.robot

robot = stretch_body.robot.Robot()
robot.startup()

ammount = sys.argv[1]

robot.end_of_arm.move_by("wrist_yaw", float(ammount))

robot.push_command()
time.sleep(1)
robot.stop()
