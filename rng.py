import numpy as np

edge = [3, 3.5, 4, 4.5, 5, 5.5, 6]

for i in range(100):
    print(i, end=' ')
    for j in range(3):
        print(edge[np.random.randint(7)], end = ' ')
    print()

# 62 6 5 3
# 57 3.5 5.5 5
# 44 6 5.5 3 
# 17 4 6 5.5
# 72 4.5 5.5 4
# 1 4.5 3.5 5
# 53 3.5 4.5 5
# 91 4 3 3
# 99 4 3 6 
# 38 6 3 4.5 