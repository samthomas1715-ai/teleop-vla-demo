from dynamixel import  Dynamixelline,DynamixelController
import config as con
import time
import calib as cb


def teleoperation():

    leader_line = Dynamixelline(con.LEADER_PORT, con.BAUDRATE)
    follower_line = Dynamixelline(con.FOLLOWER_PORT, con.BAUDRATE)

    leader = DynamixelController(con.LEADER_IDS, leader_line)
    follower = DynamixelController(con.FOLLOWER_IDS, follower_line)

    leader.tq_disb()
    follower.tq_enb()
   

    try:
        while True:
            for leader_id, follower_id in zip(con.LEADER_IDS, con.FOLLOWER_IDS):
                position = leader.get_pos(leader_id)
                fposi = follower.get_pos(follower_id)
                if abs(position - fposi) > 400:
                    break

                follower.move_to_pos(position, follower_id)
            if abs(position - fposi) > 400:
                print("Follower motor is too far from leader. Stopping teleoperation.")
                break
            

    except KeyboardInterrupt:
        print("Teleoperation stopped.")

    finally:
        follower.tq_disb()
        leader_line.closeport()
        follower_line.closeport()

teleoperation()
