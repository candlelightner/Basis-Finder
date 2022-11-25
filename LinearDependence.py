import math
from functools import partial


def addition(a, b):
    return a + b
  
def multiplication(a, b):
    return a*b

def inverse_addition(a):
    return -a

def inverse_multiplication(a):
    return 1/a

def smallest_0_mult(a):
    0

def scalar_mult(v, s):
    ret = []
    for val in v:
        ret.append(multiplication(val, s))
    return ret

def vector_add(v1, v2):
    if(len(v1) != len(v2)):
        raise ValueError("Vectors are not the same size")
    
    ret = []
    for val_i in range(len(v1)):
        ret.append(addition(v1[val_i], v2[val_i]))
    return ret

def vector_neg(v):
    return scalar_mult(v, -1)

def check_col_only_at_below(col, at):
    for i in range(at):
        if(col[i] != 0 and at != i):
            return False
        if(col[i] != 1 and at == i):
            return False
    return True

def is_linear_dep(v1, v2):
    if(len(v1) != len(v2)):
        return False
    
    v1_neg = vector_neg(v1)
    
    v1 = vector_add(v1, v1_neg)
    v2 = vector_add(v2, v1_neg)
    
    for v1_e in v1:
        for v2_e in v2:
            if(v1_e != v2_e):
                if((v1_e == 0 or v2_e == 0)):
                    return False
                if(smallest_0_mult(v1_e) != smallest_0_mult(v2_e)):
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
            if(other_col[row_i] != 0 and not is_linear_dep(col, other_col) and other_col[col_i] != col[col_i]):
                potentials.append(other_col)
    
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
                to_add = scalar_mult(s_col, inverse_multiplication(s_col[row_i]))
                to_add = scalar_mult(to_add, col[row_i])
                to_add = vector_neg(to_add)
                col = vector_add(col, to_add)
            else:
                for val in col:
                    val = multiplication(val, inverse_multiplication(col[col_i]))
                if(check_col_only_at_below(col, col_i)):
                    return matrix
                else:
                    raise ValueError("No suitable col found")
                
            matrix[col_i] = col            
                
        
        # Scale
        for val_i in range(len(col)):
            if(col[col_i] != 0):
                col[val_i] = multiplication(col[val_i], inverse_multiplication(col[col_i]))
        
    matrix[col_i] = col
    
    return matrix
        
    

def try_make_canon_basis(matrix):
    for i in matrix:
        if(len(matrix) != len(i)):
            raise ValueError("Matrix is not nxn")
    for col_i_top in range(len(matrix)):    
        #while(not check_col_only_at_below(matrix[col_i_top], col_i_top)):
        for col_i in range(len(matrix)):
            matrix = try_make_col_canon(matrix, col_i)        
    # Scale Again
    for col_i in range(len(matrix)):
        col = matrix[col_i]
        for val_i in range(len(col)):
                if(col[col_i] != 0):
                    col[val_i] = multiplication(col[val_i], inverse_multiplication(col[col_i]))
                    
    if(not check_col_only_at_below(matrix[col_i_top], col_i_top)):
        raise ValueError("Matrix is lin. dep :(")
        
    return matrix    


def transpose(matrix):
    ret = [ [0]*3 for i in range(3)]
    
    for row_i in range(len(matrix)):
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

to_test = [[5, 1, 6],
           [2, 1, 2],
           [5, 1, 6]]

to_test = transpose(to_test)
to_test = sort_matrix(to_test)


print("Starting algo for:")
print_matrix_flt(to_test)

print_matrix_str([["=", "=", "="]])

try:
    result = try_make_canon_basis(to_test)

    print("Success!!! Matrix can be transformed into canonical for using elementery operations:")
    print_matrix_str([["=", "=", "="]])
    print_matrix_flt(result)
except Exception as err:
    print("Oh no! Either your matrix is not linearily independent, or you have an error in your defenition of operations")
    print("The error is:")
    print(err)