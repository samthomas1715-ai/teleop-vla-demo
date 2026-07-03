#MuJoCo simulation - 6DOF arm.

##files -
'vx300_teleoperation' - file contains the code for for running leader and follower arm
together in synchronized manner such that follower arm's actuator(named) takes input signal into qpos(named). Therefore, whenever we move any part of the arm(ctrl + right click on mouse after selecting the part), the follower arm mimics the movement.

'vx300_inverse_kinematics' - file contains the code for the case where the coordinate of the object is known, and angles for each joint have to be calculated by newton raphson method,
such that the gripper origin reaches the object.(red ball)

'vx300_forward_kinematics' - file contains the code for the case where angles are given as input for each joint and it has to reach and print the coordinates corresponding to it.
