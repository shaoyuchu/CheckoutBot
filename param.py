import numpy as np
import math

# Serial number
SN = ''
number_of_objects = 3
# Each of inter_pos's elem is a command to move to inter_pos[i]

scan_pos = 'MOVP 30 496 150 83 -88 180'

inter_pos = ['MOVP -558 -72 -204 0 0 180',
            'MOVP -558 38 -204 0 0 180',
            'MOVP -558 148 -204 0 0 180',
            'MOVP -351 -72 -204 0 0 180',
            'MOVP -351 38 -204 0 0 180',
            'MOVP -351 148 -204 0 0 180']

def man_pose(rise, rotation):
    return 'MOVP -409 458 {} {} 0 180'.format(-200 + rise, 135.75 - rotation)

temp_pose = 'MOVP -340 337 -167 115 -81 -164'
woman_pose = 'MOVP -364 376 -241 115 -81 -164'

close_grip = 'OUTPUT 48 ON'
open_grip = 'OUTPUT 48 OFF'