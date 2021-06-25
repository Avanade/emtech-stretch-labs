import sys
import time

import stretch_body.robot

robot = stretch_body.robot.Robot()
robot.startup()

in_out = sys.argv[1]
io_move_ammount = sys.argv[2]

if in_out == "in":

    robot.arm.move_by(-1 * float(io_move_ammount))

elif in_out == "out":

    robot.arm.move_by(float(io_move_ammount))


robot.push_command()
time.sleep(4.0)

robot.stop()
