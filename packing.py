import cvxpy as cp
import numpy as np

# PARAMETERS

#   container dimensions
A = 10
B = 10
C = 10
#   number of item
n_item = 2
#   item dimensions
m = np.array([1, 2])
n = np.array([1, 2])
l = np.array([1, 2])
M = max(A, B, C) + max(np.max(m), np.max(n), np.max(l))


# VARIABLES

#   position
x = cp.Variable(n_item)
y = cp.Variable(n_item)
z = cp.Variable(n_item)
#   orientation
a = cp.Variable(n_item)
b = cp.Variable(n_item)
c = cp.Variable(n_item)
#   non-overlapping constraint variables
o1 = cp.Variable((n_item, n_item), boolean=True)
o2 = cp.Variable((n_item, n_item), boolean=True)
o3 = cp.Variable((n_item, n_item), boolean=True)
o4 = cp.Variable((n_item, n_item), boolean=True)
o5 = cp.Variable((n_item, n_item), boolean=True)
o6 = cp.Variable((n_item, n_item), boolean=True)
#   orientation-selection constraint variables
e11 = cp.Variable(n_item, boolean=True)
e12 = cp.Variable(n_item, boolean=True)
e13 = cp.Variable(n_item, boolean=True)
e21 = cp.Variable(n_item, boolean=True)
e22 = cp.Variable(n_item, boolean=True)
e23 = cp.Variable(n_item, boolean=True)
e31 = cp.Variable(n_item, boolean=True)
e32 = cp.Variable(n_item, boolean=True)
e33 = cp.Variable(n_item, boolean=True)
#   max-height variable
max_height = cp.Variable()


# CONSTRAINT
constraints = []
for i in range(n_item):

    # container size constraint
    constraints += [0 <= x[i], 0 <= y[i], 0 <= z[i]]
    constraints += [x[i] <= A - a[i], y[i] <= B - b[i], z[i] <= C - c[i]]

    # non-overlapping constraint
    for j in range(n_item):
        if j == i:
            continue
        constraints += [x[j] + a[j] - x[i] <= M * o1[i, j]]
        constraints += [x[i] - x[j] + a[i] <= M * o2[i, j]]
        constraints += [y[j] + b[j] - y[i] <= M * o3[i, j]]
        constraints += [y[i] - y[j] + b[i] <= M * o4[i, j]]
        constraints += [z[j] + c[j] - z[i] <= M * o5[i, j]]
        constraints += [z[i] - z[j] + c[i] <= M * o6[i, j]]
    
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
    constraints += [e11[i] + e12[i] + e13[i] == 1, e21[i] + e22[i] + e23[i] == 1, e31[i] + e32[i] + e33[i] == 1]
    constraints += [e11[i] + e21[i] + e31[i] == 1, e12[i] + e22[i] + e32[i] == 1, e13[i] + e23[i] + e33[i] == 1]

    # max-height constraint
    constraints += [max_height >= z[i] + c[i]]
    

# OBJECTIVE
obj = cp.Minimize(max_height)
prob = cp.Problem(obj, constraints)
prob.solve()
print("status:", prob.status)
print("max_height: ", max_height.value)
print("x.value: ", x.value)
print("y.value: ", y.value)
print("z.value: ", z.value)
