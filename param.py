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
inter_pos = [] # [ "MOVP X Y Z A B C", "MOVP X Y Z A B C", ...]