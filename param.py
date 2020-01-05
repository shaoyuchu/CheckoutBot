import numpy as np
import math

# Serial number
SN = ''
number_of_objects = 3
# Each of inter_pos's elem is a command to move to inter_pos[i]

scan_pos = 'MOVJ -2.5 -3.8 -24.6 9.9 26.7 -8.7\n'
scan_pos_inv = 'MOVJ # # # # # 171.3\n'

inter_pos = ['MOVP -558 -72 -215 0 0 180\n',
            'MOVP -351 -72 -215 0 0 180\n',
            'MOVP -558 38 -215 0 0 180\n',
            'MOVP -351 38 -215 0 0 180\n',
            'MOVP -558 148 -215 0 0 180\n',
            'MOVP -351 148 -215 0 0 180\n']
inter_pos_rise = ['MOVP -558 -72 0 0 0 180\n',
            'MOVP -351 -72 0 0 0 180\n',
            'MOVP -558 38 0 0 0 180\n',
            'MOVP -351 38 0 0 0 180\n',
            'MOVP -558 148 0 0 0 180\n',
            'MOVP -351 148 0 0 0 180\n',]

# Box size 200mm 130mm
# Need to consider the object size and dimension

packing_pose = "MOVP 495.41 -75.68 -245 -0.54 2.69 -178.876\n"
rise_packing = "MOVP # # 0 # # #\n"
pushing_pose = "MOVP 495.41 23.75 -245 # # #\n"
calib_pose = "MOVP 0 430 -195 91.382 2.781 181.137\n"
# The calib_pose is of the height of the flattest object's centroid height.

man_pose_J = "MOVJ 40.5 -82.33 40.63 0.02 -50.6 175.24\n"
man_pose_J_adj = "MOVJ 40.5 -84.5 41.3 0.02 -47.3 175.24\n"
man_pose_inv = "MOVJ 40.5 -82.33 40.63 0.02 -50.6 #\n"
man_pose_inv_adj = "MOVJ 40.5 -82.5 38.15 0.02 -47.3 #\n"
# 40.5 -82.32 40.62 0 -47.71 85.25
Rotate_gripper_90 = "MOVJ # # # # # 85.25\n"
rise_pose = "MOVP # # -50 # # #\n"
temp_pose = "MOVJ 40.5 -33.8 -22.15 0 -33.53 179.26\n"
woman_pose = 'MOVJ 40 -79.98 -5.82 -5.09 77.5 179.25\n'

close_grip = 'OUTPUT 48 ON\n'
open_grip = 'OUTPUT 48 OFF\n'

# 7x5x2

# packing gurobi

margin = 5
container_size = [150, 95, 80]
item_size = [[50, 50, 60, 60, 55, 40], [50, 45, 45, 50, 50, 30], [50, 30, 30, 30, 35, 30]]

# margin = 5
# container_size = [180, 130, 100]
# item_size = [[3, 2, 1, 3, 4, 6, 9, 1, 8, 7], [3, 2, 1, 2, 8, 1, 7, 9, 10, 6], [3, 2, 1, 1, 2, 8, 1, 7, 9, 10]]

# margin = 5
# container_size = [100, 100, 100]
# item_size = [[50, 20, 50], [30, 100, 10], [50, 20, 100]]
