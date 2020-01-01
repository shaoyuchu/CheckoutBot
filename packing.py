import cvxpy as cp
import numpy as np
from time import process_time

# ---------------------------------------- PARAMETERS ---------------------------------------- 

#   container dimensions
A = 3
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
o1 = cp.Variable((n_item, n_item), integer=True)
o2 = cp.Variable((n_item, n_item), integer=True)
o3 = cp.Variable((n_item, n_item), integer=True)
o4 = cp.Variable((n_item, n_item), integer=True)
o5 = cp.Variable((n_item, n_item), integer=True)
o6 = cp.Variable((n_item, n_item), integer=True)

#   orientation-selection constraint variables
e11 = cp.Variable(n_item, integer=True)
e12 = cp.Variable(n_item, integer=True)
e13 = cp.Variable(n_item, integer=True)
e21 = cp.Variable(n_item, integer=True)
e22 = cp.Variable(n_item, integer=True)
e23 = cp.Variable(n_item, integer=True)
e31 = cp.Variable(n_item, integer=True)
e32 = cp.Variable(n_item, integer=True)
e33 = cp.Variable(n_item, integer=True)

#   max-height variable
max_height = cp.Variable()

# ---------------------------------------- CONSTRAINT ----------------------------------------

constraints = []
for i in range(n_item):

    # container size constraint
    constraints += [0 <= x[i], 0 <= y[i], 0 <= z[i]]
    constraints += [x[i] <= A - a[i], y[i] <= B - b[i], z[i] <= C - c[i]]

    # orientation-selection constraint
    constraints += [a[i] - m[i] <= M * e11[i], m[i] - a[i] <= M * e11[i]]
    constraints += [a[i] - n[i] <= M * e12[i], n[i] - a[i] <= M * e12[i]]
    constraints += [a[i] - l[i] <= M * e13[i], l[i] - a[i] <= M * e13[i]]
    constraints += [b[i] - m[i] <= M * e21[i], m[i] - b[i] <= M * e21[i]]
    constraints += [b[i] - n[i] <= M * e22[i], n[i] - b[i] <= M * e22[i]]
    constraints += [b[i] - l[i] <= M * e23[i], l[i] - b[i] <= M * e23[i]]
    constraints += [c[i] - m[i] <= M * e31[i], m[i] - c[i] <= M * e31[i]]
    constraints += [c[i] - n[i] <= M * e32[i], n[i] - c[i] <= M * e32[i]]
    constraints += [c[i] - l[i] <= M * e33[i], l[i] - c[i] <= M * e33[i]]
    constraints += [e11[i] + e12[i] + e13[i] == 2, e21[i] + e22[i] + e23[i] == 2, e31[i] + e32[i] + e33[i] == 2]
    constraints += [e11[i] + e21[i] + e31[i] == 2, e12[i] + e22[i] + e32[i] == 2, e13[i] + e23[i] + e33[i] == 2]

    for j in range(i + 1, n_item):
        
        # non-overlapping constraint
        constraints += [x[j] - x[i] - a[i] >= -M * o1[i, j]]
        constraints += [x[i] - x[j] - a[j] >= -M * o2[i, j]]
        constraints += [y[j] - y[i] - b[i] >= -M * o3[i, j]]
        constraints += [y[i] - y[j] - b[j] >= -M * o4[i, j]]
        constraints += [z[j] - z[i] - c[i] >= -M * o5[i, j]]
        constraints += [z[i] - z[j] - c[j] >= -M * o6[i, j]]
        constraints += [o1[i, j] + o2[i, j] + o3[i, j] + o4[i, j] + o5[i, j] + o6[i, j] <= 5]

        # boolean variable constraint
        constraints += [o1[i, j] <= 1, o2[i, j] <= 1, o3[i, j] <= 1, o4[i, j] <= 1, o5[i, j] <= 1, o6[i, j] <= 1]
        constraints += [o1[i, j] >= 0, o2[i, j] >= 0, o3[i, j] >= 0, o4[i, j] >= 0, o5[i, j] >= 0, o6[i, j] >= 0]
    constraints += [e11[i] <= 1, e12[i] <= 1, e13[i] <= 1, e21[i] <= 1, e22[i] <= 1, e23[i] <= 1, e31[i] <= 1, e32[i] <= 1, e33[i] <= 1]
    constraints += [e11[i] >= 0, e12[i] >= 0, e13[i] >= 0, e21[i] >= 0, e22[i] >= 0, e23[i] >= 0, e31[i] >= 0, e32[i] >= 0, e33[i] >= 0]

    # max-height constraint
    constraints += [max_height >= z[i] + c[i]]

# ---------------------------------------- OBJECTIVE ----------------------------------------

obj = cp.Minimize(max_height)
prob = cp.Problem(obj, constraints)
prob.solve()
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
