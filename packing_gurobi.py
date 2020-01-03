import gurobipy as gp
from gurobipy import GRB
from time import process_time

container_size = [4, 2, 4]
item_size = [[2, 2, 1, 1, 1, 1], [2, 2, 1, 1, 1, 1], [2, 1, 1, 1, 1, 1]]

def packing(container_size, item_size):
    # ---------------------------------------- MODEL ---------------------------------------- 

    model = gp.Model("packing")

    # ---------------------------------------- PARAMETERS ---------------------------------------- 

    # container dimensions
    # A = 4
    # B = 2
    # C = 4

    # # number of item
    # n_item = 6

    # # item dimensions
    # m = [2, 2, 1, 1, 1, 1]
    # n = [2, 2, 1, 1, 1, 1]
    # l = [2, 1, 1, 1, 1, 1]

    A = container_size[0]
    B = container_size[1]
    C = container_size[2]

    m = item_size[0]
    n = item_size[1]
    l = item_size[2]
    
    assert len(m) == len(n)
    assert len(n) == len(l)
    n_item = len(m)

    M = max(A, B, C) + max(max(m), max(n), max(l))

    # ---------------------------------------- VARIABLES ----------------------------------------

    # position
    x = model.addVars(n_item, name='x')
    y = model.addVars(n_item, name='y')
    z = model.addVars(n_item, name='z')

    # orientation after packing
    a = model.addVars(n_item, name='a')
    b = model.addVars(n_item, name='b')
    c = model.addVars(n_item, name='c')

    # non-overlapping
    o_x = model.addVars(2, n_item, n_item, vtype=GRB.BINARY, name='o_x')
    o_y = model.addVars(2, n_item, n_item, vtype=GRB.BINARY, name='o_y')
    o_z = model.addVars(2, n_item, n_item, vtype=GRB.BINARY, name='o_z')

    # orientation-selection
    e_am = model.addVars(n_item, vtype=GRB.BINARY, name='e_am')
    e_an = model.addVars(n_item, vtype=GRB.BINARY, name='e_an')
    e_al = model.addVars(n_item, vtype=GRB.BINARY, name='e_al')
    e_bm = model.addVars(n_item, vtype=GRB.BINARY, name='e_bm')
    e_bn = model.addVars(n_item, vtype=GRB.BINARY, name='e_bn')
    e_bl = model.addVars(n_item, vtype=GRB.BINARY, name='e_bl')
    e_cm = model.addVars(n_item, vtype=GRB.BINARY, name='e_cm')
    e_cn = model.addVars(n_item, vtype=GRB.BINARY, name='e_cn')
    e_cl = model.addVars(n_item, vtype=GRB.BINARY, name='e_cl')

    #   max height
    max_height = model.addVar(name='max_height')

    # ---------------------------------------- OBJECTIVE ----------------------------------------

    model.setObjective(max_height, GRB.MINIMIZE)

    # ---------------------------------------- CONSTRAINT ----------------------------------------

    for i in range(n_item):
        # in container
        model.addConstr(x[i] <= A - a[i])
        model.addConstr(y[i] <= B - b[i])
        model.addConstr(z[i] <= C - c[i])

        # orientation selection
        model.addConstr(a[i] - m[i] <= M * e_am[i])
        model.addConstr(m[i] - a[i] <= M * e_am[i])
        model.addConstr(a[i] - n[i] <= M * e_an[i])
        model.addConstr(n[i] - a[i] <= M * e_an[i])
        model.addConstr(a[i] - l[i] <= M * e_al[i])
        model.addConstr(l[i] - a[i] <= M * e_al[i])

        model.addConstr(b[i] - m[i] <= M * e_bm[i])
        model.addConstr(m[i] - b[i] <= M * e_bm[i])
        model.addConstr(b[i] - n[i] <= M * e_bn[i])
        model.addConstr(n[i] - b[i] <= M * e_bn[i])
        model.addConstr(b[i] - l[i] <= M * e_bl[i])
        model.addConstr(l[i] - b[i] <= M * e_bl[i])

        model.addConstr(c[i] - m[i] <= M * e_cm[i])
        model.addConstr(m[i] - c[i] <= M * e_cm[i])
        model.addConstr(c[i] - n[i] <= M * e_cn[i])
        model.addConstr(n[i] - c[i] <= M * e_cn[i])
        model.addConstr(c[i] - l[i] <= M * e_cl[i])
        model.addConstr(l[i] - c[i] <= M * e_cl[i])

        model.addConstr(e_am[i] + e_an[i] + e_al[i] == 2)
        model.addConstr(e_bm[i] + e_bn[i] + e_bl[i] == 2)
        model.addConstr(e_cm[i] + e_cn[i] + e_cl[i] == 2)
        model.addConstr(e_am[i] + e_bm[i] + e_cm[i] == 2)
        model.addConstr(e_an[i] + e_bn[i] + e_cn[i] == 2)
        model.addConstr(e_al[i] + e_bl[i] + e_cl[i] == 2)
        
        # non-overlapping
        for j in range(i+1, n_item):
            model.addConstr(x[j] - x[i] - a[i] >= -M * o_x[0, i, j])
            model.addConstr(x[i] - x[j] - a[j] >= -M * o_x[1, i, j])
            model.addConstr(y[j] - y[i] - b[i] >= -M * o_y[0, i, j])
            model.addConstr(y[i] - y[j] - b[j] >= -M * o_y[1, i, j])
            model.addConstr(z[j] - z[i] - c[i] >= -M * o_z[0, i, j])
            model.addConstr(z[i] - z[j] - c[j] >= -M * o_z[1, i, j])
            model.addConstr(o_x[0, i, j] + o_x[1, i, j] + o_y[0, i, j] + o_y[1, i, j] + o_z[0, i, j] + o_z[1, i, j] <= 5)
            
        # max height
        model.addConstr(max_height >= z[i] + c[i], 'max_height')

    # ---------------------------------------- RESULT ----------------------------------------

    model.optimize()

    for var in model.getVars():
        print('%s %g' % (var.varName, var.x))

    print("\ntime: ", process_time(), "sec")
    print('Objective: %g' % model.objVal)


packing(container_size, item_size)