import numpy as np
import math
# [[x],[y],[1]]
# mapping
actual = [[-132.0847, 236.6651, 91.935104], [390.27371,411.77688, 574.30101], [1,1,1]]
img = [[469.51339957488125, 77.10519952646561,230.15167559590046], [131.64767848311172, 142.55809317365495, 315.3116258908931], [1,1,1]]
A = mapping(actual, img)

# Serial number
SN = ""
number_of_objects = 3
# Each of inter_pos's elem is a command to move to inter_pos[i]

scan_pos = "MOVP 30 496 150 83 -88 180"

inter_pos = ["MOVP -558 -72 -204 0 0 180",
            "MOVP -558 38 -204 0 0 180",
            "MOVP -558 148 -204 0 0 180",
            "MOVP -351 -72 -204 0 0 180",
            "MOVP -351 38 -204 0 0 180",
            "MOVP -351 148 -204 0 0 180"]

def man_pose(rise, rotation):
    return "MOVP -409 458 {} {} 0 180".format(-200 + rise, 135.75 - rotation)
temp_pose = "MOVP -340 337 -167 115 -81 -164"
woman_pose = "MOVP -364 376 -241 115 -81 -164"

close_grip = "OUTPUT 48 ON"
open_grip = "OUTPUT 48 OFF"