import cvxpy as cp
import numpy as np
from time import process_time

# TODO: fragility, gravity

# ---------------------------------------- PARAMETERS ---------------------------------------- 

#   container dimensions
A = 2
B = 1
C = 1

#   number of item
n_item = 2

#   item dimensions
m = np.array([1, 1])
n = np.array([1, 1])
l = np.array([1, 1])
M = max(A, B, C) + max(np.max(m), np.max(n), np.max(l))

# ---------------------------------------- VARIABLES ----------------------------------------

#   position
x = cp.Variable(n_item)
y = cp.Variable(n_item)
z = cp.Variable(n_item)

#   orientation selection
a = cp.Variable(n_item)
b = cp.Variable(n_item)
c = cp.Variable(n_item)

#   non-overlapping constraint variables
o_x1 = cp.Variable((n_item, n_item), integer=True)
o_x2 = cp.Variable((n_item, n_item), integer=True)
o_y1 = cp.Variable((n_item, n_item), integer=True)
o_y2 = cp.Variable((n_item, n_item), integer=True)
o_z1 = cp.Variable((n_item, n_item), integer=True)
o_z2 = cp.Variable((n_item, n_item), integer=True)

#   orientation-selection constraint variables
e_am = cp.Variable(n_item, integer=True)
e_an = cp.Variable(n_item, integer=True)
e_al = cp.Variable(n_item, integer=True)
e_bm = cp.Variable(n_item, integer=True)
e_bn = cp.Variable(n_item, integer=True)
e_bl = cp.Variable(n_item, integer=True)
e_cm = cp.Variable(n_item, integer=True)
e_cn = cp.Variable(n_item, integer=True)
e_cl = cp.Variable(n_item, integer=True)

#   max-height variable
max_height = cp.Variable()

# ---------------------------------------- CONSTRAINT ----------------------------------------

constraints = []
for i in range(n_item):

    # # container size constraint
    constraints += [0 <= x[i], 0 <= y[i], 0 <= z[i]]
    constraints += [x[i] <= A - a[i], y[i] <= B - b[i], z[i] <= C - c[i]]

    # # orientation-selection constraint
    constraints += [a[i] - m[i] <= M * e_am[i], m[i] - a[i] <= M * e_am[i]]
    constraints += [a[i] - n[i] <= M * e_an[i], n[i] - a[i] <= M * e_an[i]]
    constraints += [a[i] - l[i] <= M * e_al[i], l[i] - a[i] <= M * e_al[i]]
    constraints += [b[i] - m[i] <= M * e_bm[i], m[i] - b[i] <= M * e_bm[i]]
    constraints += [b[i] - n[i] <= M * e_bn[i], n[i] - b[i] <= M * e_bn[i]]
    constraints += [b[i] - l[i] <= M * e_bl[i], l[i] - b[i] <= M * e_bl[i]]
    constraints += [c[i] - m[i] <= M * e_cm[i], m[i] - c[i] <= M * e_cm[i]]
    constraints += [c[i] - n[i] <= M * e_cn[i], n[i] - c[i] <= M * e_cn[i]]
    constraints += [c[i] - l[i] <= M * e_cl[i], l[i] - c[i] <= M * e_cl[i]]
    constraints += [e_am[i] + e_an[i] + e_al[i] == 2, e_bm[i] + e_bn[i] + e_bl[i] == 2, e_cm[i] + e_cn[i] + e_cl[i] == 2]
    constraints += [e_am[i] + e_bm[i] + e_cm[i] == 2, e_an[i] + e_bn[i] + e_cn[i] == 2, e_al[i] + e_bl[i] + e_cl[i] == 2]

    for j in range(i + 1, n_item):
        
        # non-overlapping constraint
        constraints += [x[j] - x[i] - a[i] >= -M * o_x1[i, j]]
        constraints += [x[i] - x[j] - a[j] >= -M * o_x2[i, j]]
        constraints += [y[j] - y[i] - b[i] >= -M * o_y1[i, j]]
        constraints += [y[i] - y[j] - b[j] >= -M * o_y2[i, j]]
        constraints += [z[j] - z[i] - c[i] >= -M * o_z1[i, j]]
        constraints += [z[i] - z[j] - c[j] >= -M * o_z2[i, j]]
        constraints += [o_x1[i, j] + o_x2[i, j] + o_y1[i, j] + o_y2[i, j] + o_z1[i, j] + o_z2[i, j] <= 5]

        # integer variable constraint
        constraints += [o_x1[i, j] >= 0, o_x2[i, j] >= 0, o_y1[i, j] >= 0, o_y2[i, j] >= 0, o_z1[i, j] >= 0, o_z2[i, j] >= 0]
        constraints += [o_x1[i, j] <= 1, o_x2[i, j] <= 1, o_y1[i, j] <= 1, o_y2[i, j] <= 1, o_z1[i, j] <= 1, o_z2[i, j] <= 1]
    constraints += [e_am[i] >= 0, e_an[i] >= 0, e_al[i] >= 0, e_bm[i] >= 0, e_bn[i] >= 0, e_bl[i] >= 0, e_cm[i] >= 0, e_cn[i] >= 0, e_cl[i] >= 0]
    constraints += [e_am[i] <= 1, e_an[i] <= 1, e_al[i] <= 1, e_bm[i] <= 1, e_bn[i] <= 1, e_bl[i] <= 1, e_cm[i] <= 1, e_cn[i] <= 1, e_cl[i] <= 1]

    # max-height constraint
    constraints += [max_height >= z[i] + c[i]]

# ---------------------------------------- OBJECTIVE ----------------------------------------

obj = cp.Minimize(max_height)
prob = cp.Problem(obj, constraints)
prob.solve()

# print result
print("status: ", prob.status)
print("time: ", process_time(), "sec")

if max_height.value != None:
    print("Optimal maximum height: ", '%.1f'%max_height.value)
    for i in range(n_item):
        fix_zero = lambda num: 0 if abs(num) < 0.0005 else num
        print("x:", '%.1f'%x[i].value, "~", '%.1f'%(x[i].value + a[i].value))
        print("y:", '%.1f'%y[i].value, "~", '%.1f'%(y[i].value + b[i].value))
        print("z:", '%.1f'%z[i].value, "~", '%.1f'%(z[i].value + c[i].value))
        print()
