import numpy as np
from field_var import field_var

###################################
###### Your Code

val_set = {1, 2, 3, 4}

def per_cell_rules(kb, sudoku):
    """
    Generic cell rules: Determine the possible value for the cell given impossible values for this cell
    """
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
    """
    Generic 2x2 row rules: Determine the impossible values for the rest of cells in the row given a known value in this row
    """
    sudoku = np.array(sudoku)
    rows, cols = sudoku.shape
    for i in range(rows):
        for val in range(1, 5):
            for j in range(cols):
                var1 = field_var(value=val, x=i, y=j)
                other_cols = set(range(cols)).difference({j})
                for _j in other_cols:
                    prop = "{} ==> ~{}"
                    var2 = field_var(value=val, x=i, y=_j)
                    prop = prop.format(var1, var2)
                    kb.append(prop)

def per_col_rules(kb, sudoku):
    """
    Generic 2x2 column rules: Determine the impossible values for the rest of cells in the column given a known value in this column
    """
    sudoku = np.array(sudoku)
    rows, cols = sudoku.shape
    for j in range(cols):
        for val in range(1, 5):
            for i in range(rows):
                var1 = field_var(value=val, x=i, y=j)
                other_rows = set(range(rows)).difference({i})
                for _i in other_rows:
                    prop = "{} ==> ~{}"
                    var2 = field_var(value=val, x=_i, y=j)
                    prop = prop.format(var1, var2)
                    kb.append(prop)

def get_neigh_idxs(x, y, stride):
    """
    Generic method for finding neighbours in the current grid
    Return a list of neigbouring cell positions (x,y)
    """
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
    """
    Generic 2x2 grid rules: Determine the impossible values for the rest of cells in the 2x2 grid given a known value in this grid
    """
    sudoku = np.array(sudoku)
    rows, cols = sudoku.shape
    stride = np.sqrt(rows)
    for i in range(rows):
        for j in range(cols):
            for val in range(1, 5):
                var1 = field_var(value=val, x=i, y=j)
                neigh_idxs = get_neigh_idxs(i, j, stride)
                for x, y in neigh_idxs:
                    prop = "{} ==> ~{}"
                    var2 = field_var(value=val, x=x, y=y)
                    prop = prop.format(var1, var2)
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

def generate_knowledge(sudoku):
    kb = []
    # DONE: Fill kb with propositions
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

    return kb

###################################