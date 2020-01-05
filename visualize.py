import matplotlib.pyplot as plt
import numpy as np
import glob
import os
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image


def gifGenerator(filenames):
    frames = []
    for i in filenames:
        new_frame = Image.open(i)
        frames.append(new_frame)
    
    frames[0].save('visualization/gif.gif', format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=1000)
    print('visualization/gif.gif saved')


def visualize(seq, container_size, x_pos, y_pos, z_pos, a_len, b_len, c_len, shrink_ratio=5):

    if shrink_ratio != 1:
        shrink = lambda li: list(map(lambda length: int(length/shrink_ratio), li))
        container_size = shrink(container_size)
        x_pos, y_pos, z_pos = shrink(x_pos), shrink(y_pos), shrink(z_pos)
        a_len, b_len, c_len = shrink(a_len), shrink(b_len), shrink(c_len)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlabel("x (5mm)")
    ax.set_ylabel("y (5mm)")
    ax.set_zlabel("z (5mm)")
    filled = np.zeros(tuple(container_size), dtype=bool)

    filenames = []
    files = glob.glob('visualization/*')
    for f in files:
        os.remove(f)
    for i in range(len(seq)):
        filled[x_pos[seq[i]]:x_pos[seq[i]] + a_len[seq[i]], y_pos[seq[i]]:y_pos[seq[i]] + b_len[seq[i]], z_pos[seq[i]]:z_pos[seq[i]] + c_len[seq[i]]] = True
        ax.voxels(filled, facecolors='#FFD65DC0', alpha=0.8)
        filenames.append('visualization/%d.png'%i)
        plt.savefig(filenames[-1])
        print(filenames[-1], 'saved')
    gifGenerator(filenames)


if __name__ == "__main__":

    container_size = [150, 95, 80]
    x_pos = [95, 50, 0, 85, 35, 0]
    y_pos = [0, 40, 55, 55, 0, 0]
    z_pos = [0, 0, 0, 0, 0, 0]
    a_len = [55, 35, 50, 65, 55, 35]
    b_len = [55, 55, 35, 35, 40, 45]
    c_len = [55, 50, 65, 55, 60, 35]

    imgs = visualize(seq, container_size, x_pos, y_pos, z_pos, a_len, b_len, c_len, shrink_ratio=5)