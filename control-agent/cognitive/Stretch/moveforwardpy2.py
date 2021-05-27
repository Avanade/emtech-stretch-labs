#python 2.7

import stretch_body.robot
robot=stretch_body.robot.Robot()
robot.startup()

robot.base.trasnlate_by(0.1)
robot.push_command()


robot.stop()