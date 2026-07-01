from gitdynamixel import  Dynamixelline,DynamixelController
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
            positions = leader.get_pos()

            #if follower and leader have diff ids
            follower_positions = {}
            for leader_id, follower_id in zip(con.LEADER_IDS, con.FOLLOWER_IDS):
                follower_positions[follower_id] = positions[leader_id]

            follower.move_all_to_pos(follower_positions)
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Teleoperation stopped.")

    finally:
        follower.tq_disb()
        leader_line.port.closePort()
        follower_line.port.closePort()