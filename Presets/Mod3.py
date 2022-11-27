def addition(a, b):
    return (a + b) % 3
  
def multiplication(a, b):
    return (a*b) % 3

def inverse_addition(a):
    return -a

def inverse_multiplication(a):
    return a

#use math.lcm if you want to find out the least common multiple of any amount of numbers
def smallest_0_mult(a):
    return (math.lcm(3, a))/a # 3 is prime, so it's always a*3

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
    return x % 3