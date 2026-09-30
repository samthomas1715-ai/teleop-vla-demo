import torch
import cv2
import numpy as np
from lerobot.datasets import LeRobotDataset


from dynamixel import DynamixelLine, DynamixelController
import config as con
import time
import calib as cb
from dynamixel_sdk import GroupSyncWrite, DXL_LOBYTE, DXL_HIBYTE

def record_teleop():
    
    cap_high = cv2.VideoCapture(0) 
    cap_gripper = cv2.VideoCapture(2)
    ret_h, frame_h = cap_high.read()
    ret_g, frame_g = cap_gripper.read()

    if not ret_h or not ret_g:
        print("Failed to grab camera. Check connection.")
        return
    high_h, high_w, high_c = frame_h.shape
    grip_h, grip_w, grip_c = frame_g.shape
    
    
    leader_line = DynamixelLine(con.LEADER_PORT, con.BAUDRATE)
    follower_line = DynamixelLine(con.FOLLOWER_PORT, con.BAUDRATE)
    leader = DynamixelController(con.LEADER_IDS, leader_line)
    follower = DynamixelController(con.FOLLOWER_IDS, follower_line)

    leader.tq_disb()
    follower.tq_enb()
    sync_write = GroupSyncWrite(follower_line.port, follower_line.packethandler, con.ADDR_GOAL_POSITION, 2)
    
    
    num_joints = len(con.LEADER_IDS)
    features = {
        "observation.images.cam_high": {"dtype": "video", "shape": [high_h, high_w, high_c], "names": ["height", "width", "channels"]},
        "observation.images.cam_gripper": {"dtype": "video", "shape": [grip_h, grip_w, grip_c], "names": ["height", "width", "channels"]},
        "observation.state": {"dtype": "float32", "shape": [num_joints], "names": ["joint_angles"]},
        "action": {"dtype": "float32", "shape": [num_joints], "names": ["joint_commands"]}
    }

    dataset = LeRobotDataset.create(
        repo_id="my_local_teleop_dataset",
        fps=30, 
        features=features,
        local_files_only=True
    )

    print("Ready, Press 's' to save an episode, 'q' to quit.")

    try:
        while True:

            ret_h, bgr_high = cap_high.read()
            ret_g, bgr_gripper = cap_gripper.read()

            if not ret_h or not ret_g:
                break
                
            current_state = []
            target_action = []
            safety_triggered = False

    
            for leader_id, follower_id in zip(con.LEADER_IDS, con.FOLLOWER_IDS):
                position = leader.get_pos(leader_id)
                fposi = follower.get_pos(follower_id)
                
                if position is None or fposi is None:
                    continue
                    
                if abs(position - fposi) > 400:
                    safety_triggered = True
                    break
                    
               
                current_state.append(fposi)
                target_action.append(position)
                
                param_goal_position = [DXL_LOBYTE(position), DXL_HIBYTE(position)]
                sync_write.addParam(follower_id, param_goal_position)

            if safety_triggered:
                print("Follower motor is too far from leader. Stopping teleoperation.")
                break
                
            
            if len(current_state) != num_joints:
                sync_write.clearParam()
                continue

            
            sync_write.txPacket()
            sync_write.clearParam()
            
            
            rgb_high = cv2.cvtColor(bgr_high, cv2.COLOR_BGR2RGB)
            rgb_gripper = cv2.cvtColor(bgr_gripper, cv2.COLOR_BGR2RGB)
            frame_dict = {
                "observation.images.cam_high": torch.from_numpy(rgb_high),
                "observation.images.cam_gripper": torch.from_numpy(rgb_gripper),
                "observation.state": torch.tensor(current_state, dtype=torch.float32),
                "action": torch.tensor(target_action, dtype=torch.float32)
            }
            dataset.add_frame(frame_dict)
    
            cv2.imshow("Teleop View_high", bgr_high)
            cv2.imshow("teleop view_grip", bgr_gripper)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('s'):
                
                dataset.save_episode(task="Pick up the object") 
                print("Episode saved! You can start the next demonstration.")
            elif key == ord('d'):
                dataset.clear_episode_buffer()
                print("wrong recording deleted")
            elif key == ord('q'):
                break

    except KeyboardInterrupt:
        print("Teleoperation interrupted by user.")
        
    finally:

        print("Consolidating dataset... do not close terminal.")
        dataset.consolidate()
        
        cap_high.release()
        cap_gripper.release()
        cv2.destroyAllWindows()
        follower.tq_disb()
        leader_line.closeport()
        follower_line.closeport()
        print("Hardware safely shut down.")

if __name__ == "__main__":
    record_teleop()
