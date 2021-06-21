import stretch_body.robot
import time
import sys

robot = stretch_body.robot.Robot()
robot.startup()

print("recieved:", sys.argv[1])


robot.end_of_arm.move_by("wrist_yaw", float(sys.argv[1]))

robot.push_command()
time.sleep(1)
robot.stop()
