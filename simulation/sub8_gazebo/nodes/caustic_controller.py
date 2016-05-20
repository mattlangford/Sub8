#!/usr/bin/env python
import rospy
import tf

from std_msgs.msg import String
from gazebo_msgs.msg import ContactsState, ModelStates, ModelState
from gazebo_msgs.srv import SetModelState, GetModelState, SetModelStateRequest
from geometry_msgs.msg import Pose, Twist
from sub8_msgs.srv import SetValve

from sub8_ros_tools import msg_helpers, geometry_helpers

import numpy as np

'''
A caustic image is projected from the projector then the whole projector is moved around really
    quickly to generate moving caustics.
TODO: Figure out how to change projector image.
'''


def move_it(set_state):
    # Generate the pose
    scale = 50
    position = np.random.uniform(-1, 1, size=3) * scale
    position[2] = 250  # meters up in the sky

    orientation = tf.transformations.random_quaternion()
    orientation[:2] = 0

    pose = msg_helpers.numpy_quat_pair_to_pose(position, orientation)

    # Generate the message
    projector_name = 'projector_model'
    s = SetModelStateRequest()
    m = ModelState()
    m.model_name = projector_name
    m.pose = pose
    s.model_state = m

    set_state(s)

if __name__ == '__main__':
    rospy.init_node('caustic_controller')
    set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
    rospy.Timer(rospy.Duration(.075), lambda move: move_it(set_state))
    rospy.spin()