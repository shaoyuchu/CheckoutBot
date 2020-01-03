import cv2
import numpy as np
import queue
from param import *
import pandas as pd

# grabbing (int, int)

def traceRoute(s, ind, SN, face, grabbing):
    # edges = [7, 5, 3], face = (7, 3), grabbing = 3
    df = pd.read_csv("./obj_data/obj_info.csv")
    edges = df.iloc[SN - 1][1:4].to_numpy()
    face = (max(face), min(face))
    
    
    if edges[0] == face[0] and edges[1] == face[1]:
        # 7 5
        if grabbing == face[0]:
            print("***** 1-1 *****")
            s.sendall(inter_pos[ind].encode('ascii'))
            input("check this face...")
            s.sendall(open_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            # grabbing 7
            # do nothing
        else:
            print("***** 1-2 *****")
            s.sendall(man_pose_J.encode('ascii'))
            s.sendall(open_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            s.sendall(Rotate_gripper_90.encode('ascii'))
            s.sendall(man_pose_inv.encode('ascii'))
            s.sendall(close_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            s.sendall(inter_pos[ind].encode('ascii'))
            s.sendall(open_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))

            # grabbing 5
            # release, rotate, grab
            pass
        
    elif edges[1] == face[0] and edges[2] == face[1]:
        # 53
        if grabbing == face[0]:
            print("***** 2-1 *****")
            # grabbing 5
            # rotate 90, release, woman pose, done
            s.sendall(man_pose_J.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            s.sendall(Rotate_gripper_90.encode('ascii'))
            s.sendall(man_pose_inv.encode('ascii'))
            s.sendall(open_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            s.sendall(temp_pose.encode('ascii'))
            s.sendall(woman_pose.encode('ascii'))
            s.sendall(close_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            s.sendall(inter_pos[ind].encode('ascii'))
            s.sendall(open_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))

            pass
        else:
            print("***** 2-2 *****")
            # grabbing 3
            s.sendall(man_pose_J.encode('ascii'))
            s.sendall(open_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            s.sendall(temp_pose.encode('ascii'))
            s.sendall(woman_pose.encode('ascii'))
            s.sendall(close_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            s.sendall(inter_pos[ind].encode('ascii'))
            s.sendall(open_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            # release, rise, rotate, aprroach, grab, and do grabbing 5
            pass
    else:
        # 73
        if grabbing == face[0]:
            print("***** 3-1 *****")
            # grabbing 7
            # go to woman pose, grab 5, do grabbing 5
            s.sendall(man_pose_J.encode('ascii'))
            s.sendall(Rotate_gripper_90.encode('ascii'))
            s.sendall(open_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            s.sendall(temp_pose.encode('ascii'))
            s.sendall(woman_pose.encode('ascii'))
            s.sendall(close_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            s.sendall(man_pose_J.encode('ascii'))
            s.sendall(open_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            s.sendall(Rotate_gripper_90.encode('ascii'))
            s.sendall(man_pose_inv.encode('ascii'))
            s.sendall(close_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            s.sendall(inter_pos[ind].encode('ascii'))
            s.sendall(open_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))

        else:
            print("***** 3-2 *****")
            s.sendall(man_pose_J.encode('ascii'))
            s.sendall(open_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            s.sendall(temp_pose.encode('ascii'))
            s.sendall(woman_pose.encode('ascii'))
            s.sendall(close_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            s.sendall(man_pose_J.encode('ascii'))
            s.sendall(open_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            s.sendall(Rotate_gripper_90.encode('ascii'))
            s.sendall(man_pose_inv.encode('ascii'))
            s.sendall(close_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            s.sendall(inter_pos[ind].encode('ascii'))
            s.sendall(open_grip.encode('ascii'))
            s.sendall(rise_pose.encode('ascii'))
            # grabbing 3
            # rotate to grab 7, do the rest as grabbing 7
            pass