import math
from functools import partial

import importlib
import importlib.util
import sys
from os.path import exists

def is_square(matrix):
    for i in matrix:
        if(len(matrix) != len(i)):
            return False
    return True

def field_transform(matrix):
    if(is_square(matrix)):
        for col_i in range(len(matrix)):
            col = matrix[col_i]
            for row_i in range(len(col)):
                col[row_i] = preset.transform(col[row_i])
            matrix[col_i] = col
    return matrix

def check_col_only_at_below(col, at):
    if(col[at] == 0):
        return False
    for i in range(at):
        if(preset.transform(col[i]) != 0 and at != i):
            return False
        if(preset.transform(col[i]) != 1 and at == i):
            return False
    return True

def is_linear_dep(v1, v2):
    if(len(v1) != len(v2)):
        return False
    
    v1_neg = preset.vector_neg(v1)
    
    v1 = preset.vector_add(v1, v1_neg)
    v2 = preset.vector_add(v2, v1_neg)
    
    for v1_e in v1:
        for v2_e in v2:
            if(preset.transform(v1_e) != preset.transform(v2_e)):
                if((preset.transform(v1_e) == 0 or transform(v2_e) == 0)):
                    return False
                if(preset.smallest_0_mult(v1_e) != preset.smallest_0_mult(v2_e)):
                    return False
    
    return True

def potential_metric(potential, col):
    ret = 0
    
    for val_i in range(len(potential)):
        if(potential[val_i] == 0 and col[val_i] ==0):
            ret += 1
            
    return ret

def sort_potentials(potentials, col):
    potentials.sort(key=partial(potential_metric, col=col), reverse=True)
    return potentials

def find_suitable_col(matrix, col_i, row_i):
    col = matrix[col_i]
    
    potentials = []
    
    for other_col_i in range(len(matrix)):
        if(other_col_i != col_i):
            other_col = matrix[other_col_i]
            if(other_col[row_i] != 0 and not is_linear_dep(col, other_col) and preset.transform(other_col[col_i]) != preset.transform(col[col_i])):
                potentials.append(other_col)
    
    if(len(potentials) == 0):
        raise ValueError("No suitable col found, matrix might be lin. dep.")
    
    return sort_potentials(potentials, col)[0]
    
                
                

def try_make_col_canon(matrix, col_i):
    col = matrix[col_i]
    
    if(check_col_only_at_below(col, col_i)):
        return matrix
    
    for row_i in range(col_i):
        if(row_i != col_i and col[row_i] != 0):
            # Find suitable col for "subtraction"
            s_col = find_suitable_col(matrix, col_i, row_i)
            
            if(s_col is not None):
                to_add = preset.scalar_mult(s_col, preset.inverse_multiplication(s_col[row_i]))
                to_add = preset.scalar_mult(to_add, col[row_i])
                to_add = preset.vector_neg(to_add)
                col = preset.vector_add(col, to_add)
            else:
                for val in col:
                    val = preset.multiplication(val, preset.inverse_multiplication(col[col_i]))
                if(check_col_only_at_below(col, col_i)):
                    return matrix
                else:
                    raise ValueError("No suitable col found")
                
            matrix[col_i] = col            
                
        
        # Scale
        inverse = preset.inverse_multiplication(col[col_i])
        
        if(inverse != 0):
            for val_i in range(len(col)):
                dbg = preset.inverse_multiplication(col[col_i])
                col[val_i] = preset.multiplication(col[val_i], inverse)
        
    matrix[col_i] = col
    
    return matrix
        
    

def try_make_canon_basis(matrix):
    if(not is_square(matrix)):
        raise ValueError("Matrix is not nxn")
      
    for col_i in range(len(matrix)):
        matrix = try_make_col_canon(matrix, col_i)
        
        matrix = field_transform(matrix)
        
        tmp = sort_matrix(matrix)
        
        if(tmp != matrix):
            matrix = tmp
            col_i = 0
        
    # Scale Again
    for col_i in range(len(matrix)):
        col = matrix[col_i]
        for val_i in range(len(col)):
                if(col[col_i] != 0):
                    col[val_i] = preset.multiplication(col[val_i], preset.inverse_multiplication(col[col_i]))
    
    for col_i in range(len(matrix)):
        if(not check_col_only_at_below(matrix[col_i], col_i)):
            raise ValueError("Matrix is lin. dep :(")
        
    matrix = field_transform(matrix)
        
    return matrix    

def add_not_0_at_i(matrix, col_i):
    col = matrix[col_i]
    
    if(col[col_i] != 0):
        return matrix
    
    for other_col in matrix:
        if(other_col[col_i] != 0):
            matrix[col_i] = preset.vector_add(other_col, col)
            return matrix

def make_matrix_not_0(matrix):
    for col_i in range(len(matrix)):
        matrix = add_not_0_at_i(matrix, col_i)
    return matrix

def transpose(matrix):
    len_matrix = len(matrix)
    ret = [ [0]*len_matrix for i in range(len_matrix)]
    
    for row_i in range(len_matrix):
        for col_i in range(len(matrix[row_i])):
            ret[col_i][row_i] = matrix[row_i][col_i]
            
    return ret

def amt_non_0(v):
    i = 0
    
    len_v = len(v)
    
    for v_i in range(len_v):
        if(v[v_i] != 0):
            i += len_v - v_i/2
    return i

def sort_matrix(matrix):
    matrix.sort(key=amt_non_0, reverse=True)
    return matrix

def print_matrix_str(matrix):
    for i in matrix:
        print('\t'.join(map(str, i)))
        
def format(input):
    return str("{:.2f}".format(input))
        
def print_matrix_flt(matrix):
    for i in matrix:
        print('\t'.join(map(format, i)))

module_name = input("Enter a name of your preset file (in /Presets), leave empty for default: ")

if module_name in sys.modules:
    pass
elif (importlib.util.spec_from_file_location(f"{module_name}", f"./Presets/{module_name}.py")) is not None and exists(f"./Presets/{module_name}.py"):
    spec = importlib.util.spec_from_file_location(f"{module_name}", f"./Presets/{module_name}.py")
    preset = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = preset
    spec.loader.exec_module(preset)
    print(f"{module_name!r} has been imported")
else:
    print(f"Can't find the {module_name} module, using default")
    module_name = None

if(module_name is None):
    spec = importlib.util.spec_from_file_location("Default", "./Presets/Default.py")
    preset = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = preset
    spec.loader.exec_module(preset)

to_test = [[1, -1],
           [-1, 1]]

to_test = transpose(to_test)
to_test = sort_matrix(to_test)
to_test = make_matrix_not_0(to_test)

print("Starting algo for:")
print_matrix_flt(transpose(to_test))

print_matrix_str([["="]*len(to_test)])

try:
    result = try_make_canon_basis(to_test)

    result = transpose(result)

    print("Success!!! Matrix can be transformed into canonical form using elementary operations:")
    print_matrix_str([["=", "=", "="]])
    print_matrix_flt(result)
except Exception as err:
    print("Oh no! Either your matrix is not linearily independent, or you have an error in the definition of your operations")
    print("The error is:")
    print(err)