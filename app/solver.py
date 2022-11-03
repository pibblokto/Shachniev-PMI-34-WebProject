import random

def Multiply(size, minval, maxval):
    a = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(random.randint(minval, maxval))
        a.append(row)
    b = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(random.randint(minval, maxval))
        b.append(row)
    result_sum = 0
    for i in range(size):
       for j in range(size):
           for k in range(size):
               result_sum += a[i][k] * b[k][j]
    return round(result_sum / size**2, 2)