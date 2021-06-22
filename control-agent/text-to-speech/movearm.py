import sys
import time

import stretch_body.robot

robot = stretch_body.robot.Robot()
robot.startup()

up_down = sys.argv[1]
ud_move_amount = sys.argv[1]
in_out = sys.argv[3]
io_move_ammount = sys.argv[4]

if in_out == "in":

    robot.arm.move_by(-1 * float(io_move_ammount))

elif in_out == "out":

    robot.arm.move_by(float(io_move_ammount))

if up_down == "up":
    robot.lift.move_by(float(ud_move_amount))

elif up_down == "down":
    robot.lift.move_by(-1 * float(ud_move_amount))

robot.push_command()
time.sleep(4.0)

robot.stop()
