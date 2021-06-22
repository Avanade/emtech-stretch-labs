import sys
import time

import stretch_body.robot

robot = stretch_body.robot.Robot()
robot.startup()


if sys.argv[3] == "in":

    robot.arm.move_by(-1 * float(sys.argv[4]))

elif sys.argv[3] == "out":

    robot.arm.move_by(float(sys.argv[4]))

if sys.argv[1] == "up":
    robot.lift.move_by(float(sys.argv[2]))

elif sys.argv[1] == "down":
    robot.lift.move_by(-1 * float(sys.argv[2]))

robot.push_command()
time.sleep(4.0)

robot.stop()
