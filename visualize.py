import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

shrink = lambda li: list(map(lambda len: int(len / 5), li))
container_size = shrink([150, 95, 80])
x_pos = shrink([95, 50, 0, 85, 35, 0])
y_pos = shrink([0, 40, 55, 55, 0, 0])
z_pos = shrink([0, 0, 0, 0, 0, 0])
a_len = shrink([55, 35, 50, 65, 55, 35])
b_len = shrink([55, 55, 35, 35, 40, 45])
c_len = shrink([55, 50, 65, 55, 60, 35])

def visualize(container_size, x_pos, y_pos, z_pos, a_len, b_len, c_len):

    voxels = np.zeros(tuple(container_size), dtype=bool)
    n_item = len(x_pos)
    for i in range(n_item):
        voxels[x_pos[i]:x_pos[i] + a_len[i], y_pos[i]:y_pos[i] + b_len[i], z_pos[i]:z_pos[i] + c_len[i]] = True
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlabel("x (5mm)")
    ax.set_ylabel("y (5mm)")
    ax.set_zlabel("z (5mm)")
    ax.voxels(voxels, facecolors='#FFD65DC0')

    plt.savefig('visualization.png')

visualize(container_size, x_pos, y_pos, z_pos, a_len, b_len, c_len)
