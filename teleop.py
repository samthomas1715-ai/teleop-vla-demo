from dynamixel import  Dynamixelline,DynamixelController
import config as con
import time

def teleoperation():

    leader_line = Dynamixelline(con.LEADER_PORT, con.BAUDRATE)
    follower_line = Dynamixelline(con.FOLLOWER_PORT, con.BAUDRATE)

    leader = DynamixelController(con.LEADER_IDS, leader_line)
    follower = DynamixelController(con.FOLLOWER_IDS, follower_line)

    leader.tq_disb()
    follower.tq_enb()

    try:
        while True:
            leader_pos = leader.get_pos()
            goal_positions = {}
            delta = {}

            for leader_id in con.LEADER_IDS:
                delta[leader_id] = leader_pos[leader_id] - cb.FOLLOWER_HOME[leader_id]
      
            for leader_id, follower_id in zip(con.LEADER_IDS, con.FOLLOWER_IDS):
                goal_positions[follower_id] = cb.FOLLOWER_HOME[follower_id] + delta[leader_id]
            #check direction of rotation of the motors

            follower.move_all_to_pos(goal_positions)
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Teleoperation stopped.")

    finally:
        follower.tq_disb()
        leader_line.closeport()
        follower_line.closeport()
