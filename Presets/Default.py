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

def transform(x):
    return x