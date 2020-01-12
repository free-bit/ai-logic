import numpy as np
from field_var import field_var

###################################
###### Your Code

val_set = {1, 2, 3, 4}

def per_cell_rules(kb, sudoku):
    sudoku = np.array(sudoku)
    rows, cols = sudoku.shape
    for i in range(rows):
        for j in range(cols):
            for val in range(1, 5):
                prop = "~{} & ~{} & ~{} ==> {}"
                atoms = []
                vals_left = val_set.difference({val})

                for val_left in vals_left:
                    var = field_var(value=val_left, x=i, y=j)
                    atoms.append(var)
                var = field_var(value=val, x=i, y=j)
                atoms.append(var)

                prop = prop.format(*atoms)
                kb.append(prop)

def per_row_rules(kb, sudoku):
    sudoku = np.array(sudoku)
    rows, cols = sudoku.shape
    for i in range(rows):
        for val in range(1, 5):
            for j in range(cols):
                prop = "~{} & ~{} & ~{} ==> {}"
                atoms = []
                other_cols = set(range(cols)).difference({j})
                for _j in other_cols:
                    atom = field_var(value=val, x=i, y=_j)
                    atoms.append(atom)
                var = field_var(value=val, x=i, y=j)
                atoms.append(var)
                prop = prop.format(*atoms)
                kb.append(prop)

def per_col_rules(kb, sudoku):
    sudoku = np.array(sudoku)
    rows, cols = sudoku.shape
    for j in range(cols):
        for val in range(1, 5):
            for i in range(rows):
                prop = "~{} & ~{} & ~{} ==> {}"
                atoms = []
                other_rows = set(range(rows)).difference({i})
                for _i in other_rows:
                    atom = field_var(value=val, x=_i, y=j)
                    atoms.append(atom)
                var = field_var(value=val, x=i, y=j)
                atoms.append(var)
                prop = prop.format(*atoms)
                kb.append(prop)

def get_neigh_idxs(x, y, stride):
    idxs = []

    # along x
    x_offset = x % stride
    
    # along y
    y_offset = y % stride

    # Conditions
    not_top = x_offset >= 1
    not_left = y_offset >= 1
    not_bottom = x_offset < stride-1
    not_right = y_offset < stride-1

    if not_top and not_left:
        idxs.append((x-1, y-1))
    if not_top:
        idxs.append((x-1, y))
    if not_top and not_right:
        idxs.append((x-1, y+1))
    if not_left:
        idxs.append((x, y-1))
    if not_right:
        idxs.append((x, y+1))
    if not_bottom and not_left:
        idxs.append((x+1, y-1))
    if not_bottom:
        idxs.append((x+1, y))
    if not_bottom and not_right:
        idxs.append((x+1, y+1))

    return idxs

def per_grid_rules(kb, sudoku):
    sudoku = np.array(sudoku)
    rows, cols = sudoku.shape
    stride = np.sqrt(rows)
    for i in range(rows):
        for j in range(cols):
            for val in range(1, 5):
                prop = "~{} & ~{} & ~{} ==> {}"
                atoms = []
                neigh_idxs = get_neigh_idxs(i, j, stride)
                for x, y in neigh_idxs:
                    atom = field_var(value=val, x=x, y=y)
                    atoms.append(atom)
                var = field_var(value=val, x=i, y=j)
                atoms.append(var)
                prop = prop.format(*atoms)
                kb.append(prop)

def store_init_state(kb, sudoku):
    """
    Stores initial state of the sudoku
    """
    sudoku = np.array(sudoku)
    x, y = np.nonzero(sudoku)
    vals = sudoku[x, y]
    for i in range(len(vals)):
        prop = field_var(value=int(vals[i]), x=int(x[i]), y=int(y[i]))
        kb.append(prop)

def rows_check(kb, sudoku):
    """
    Checks rows of sudoku
    """
    sudoku = np.array(sudoku)
    for i, row in enumerate(sudoku):
        vals = row[row != 0]
        col_idxs = np.where(row == 0)[0]
        for col_idx in col_idxs:
            for val in vals:
                prop = "~" + field_var(value=int(val), x=i, y=int(col_idx))
                kb.append(prop)

def cols_check(kb, sudoku):
    """
    Checks rows of sudoku.T, i.e. cols of sudoku
    """
    sudoku = np.array(sudoku).T
    for j, col in enumerate(sudoku):
        vals = col[col != 0]
        row_idxs = np.where(col == 0)[0]
        for row_idx in row_idxs:
            for val in vals:
                prop = "~" + field_var(value=int(val), x=int(row_idx), y=j)
                kb.append(prop)

def grids_check(kb, sudoku):
    """
    Checks 2x2 grids of sudoku
    """
    sudoku = np.array(sudoku)
    x_size, y_size = sudoku.shape
    u_size, v_size = 2, 2
    for i in range(0, x_size, u_size):
        for j in range(0, y_size, v_size):
            grid = sudoku[i:i+u_size, j:j+v_size]
            vals = grid[grid != 0]
            idxs = zip(*np.where(grid == 0))
            for x, y in idxs:
                for val in vals:
                    prop = "~" + field_var(value=int(val), x=int(i+x), y=int(j+y))
                    kb.append(prop)


def generate_knowledge(sudoku):
    # TODO generate the Knowledge Base
    # you can assume the sudoku is always a 4x4 array. 
    # Feel free to add helper functions in this file if you need them
    # Do not change any other notebooks or files only this file will be evaluated in the end.
    # It is also the only file you need to submit
    # Do not import any additional module or packages
    kb = []
    # TODO fill kb with propositions
    print("Adding per cell rules...")
    per_cell_rules(kb, sudoku)
    
    print("Adding per row rules...")
    per_row_rules(kb, sudoku)
    
    print("Adding per column rules...")
    per_col_rules(kb, sudoku)
    
    print("Adding per grid rules...")
    per_grid_rules(kb, sudoku)
    
    print("Adding per initial state...")
    store_init_state(kb, sudoku)
    # rows_check(kb, sudoku)
    # cols_check(kb, sudoku)
    # grids_check(kb, sudoku)
    return kb

###################################