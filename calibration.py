from gitdynamixel import Dynamixelline, DynamixelController
import config as con


def calibrate():

    leader_line = Dynamixelline(con.LEADER_PORT, con.BAUDRATE)
    follower_line = Dynamixelline(con.FOLLOWER_PORT, con.BAUDRATE)

    leader = DynamixelController(con.LEADER_IDS, leader_line)
    follower = DynamixelController(con.FOLLOWER_IDS, follower_line)

    leader.tq_disb()
    follower.tq_disb()

    print("\CALIBRATION...")
    #print("Move both arms into the same physical home position.")
    input("Press ENTER when ready...")
 
    #reading home positions
    leader_home = leader.get_pos()
    follower_home = follower.get_pos()

    #save home positions
    with open("calibration_data.py", "w") as file:
        file.write(f"LEADER_HOME = {leader_home}\n\n")
        file.write(f"FOLLOWER_HOME = {follower_home}\n")

    print("\nCalibration Successful!")
    print("Leader Home :", leader_home)
    print("Follower Home :", follower_home)

    # Close ports
    leader_line.closeport()
    follower_line.closeport()

if __name__ == "__main__":
    calibrate()