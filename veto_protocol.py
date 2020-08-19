import random 
import functools
from fractions import Fraction

# Helper function to print a matrix nicely
def show(intro, mat):
    print("\n" + intro)
    
    if isinstance(mat[0], int):
        print(mat)
        return 0

    n = len(mat)
    m = len(mat[0])
    for i in range(n):
        for j in range(m):
            print(mat[i][j], end = " " if j < m - 1 else "\n")

# Class encapsulating Pedersen commitment parameters            
class Pedersen:
    # p, q primes such that p | q - 1
    # G = {i^r mod q | i in Z_q* = {1,...,q-1}}    
    p =  23 # Order of G
    q =  47 # Operations inside G need to be executed modulus q
    # Generators of G
    g =  42
    h =  4
        
pedersen = Pedersen()

# Bids by party by bits
generate_bids_randomly = True

if not(generate_bids_randomly):   
    p = [[0,1,0,1,0],
         [0,1,0,0,1],
         [0,0,1,1,1]]
else:
    n = 3
    m = 5
    p = [[random.randint(0, 1) for j in range(m)] for i in range(n)]

show("p = ", p)

n = len(p)
m = len(p[0])

# Declared bids by party by bits
d = [[0 for j in range(m)] for i in range(n)]

# Veto per round
v = [0 for i in range(m)]

# Random elements of Z_p used for commitments
x = [[random.randint(1,pedersen.p - 1) for j in range(m)] for i in range(n)]
r = [[random.randint(1,pedersen.p - 1) for j in range(m)] for i in range(n)]

# Commitments 
# X, R and Y are precomputed to simplify the script
# In the actual protocol they should be computed and published by the parties at each round

X = [[pedersen.g**x[i][j] for j in range(m)] for i in range(n)]
R = [[pedersen.g**r[i][j] for j in range(m)] for i in range(n)]

# Helper functions to compute Y
def prod(vec):
    return functools.reduce(lambda a, b: a*b, vec, 1)

def col(mat, index):
    return [e[index] for e in mat]

Y = [[Fraction(prod(col(X,j)[0:i]) , prod(col(X,j)[i+1:n])) for j in range(m)] for i in range(n)]        
b = [[0 for j in range(m)] for i in range(n)]

# Index of last veto (initialized to -1 arbitrarily)
j_backarrow = -1

# Veto protocol
for j in range(m): # Rounds
    print("\nRound " + str(j))
    print("j_backarrow = " + str(j_backarrow))
    for i in range(n): # Parties
        
        if j_backarrow == -1: # No veto so far
            d[i][j] = p[i][j]
        else: # At least one veto
            d[i][j] = 1 if p[i][j] and d[i][j_backarrow] == 1 else 0
            
        print("Party " + str(i) + " : p = " + str(p[i][j]) + " d* = " + str(d[i][j_backarrow]) + " d = " + str(d[i][j]))
        
        # Compute result of veto protocol assuming d[i][j] is available
        # In the actual protocol commitments have to be used instead
        v[j] = 1 if v[j] or d[i][j] == 1 else 0
        
        # Commit b according to d[i][j]
        if d[i][j] == 1:
            b[i][j] = R[i][j]**x[i][j]
        else:
            b[i][j] = Y[i][j]**x[i][j]
        
        # Check logical conditions guaranteeing that parties are following the protocol
        # In the actual protocol ZKP have to be used instead
        if j_backarrow == -1:
            # c0 must hold until first veto
            c0 = p[i][j] == d[i][j]
            assert(c0)
        else:            
            # c1 or c2 or c3 must hold after first veto
            c1 = p[i][j] == 0 and d[i][j] == 0
            c2 = p[i][j] == 1 and d[i][j_backarrow] == 1 and d[i][j] == 1
            c3 = p[i][j] == 1 and d[i][j_backarrow] == 0 and d[i][j] == 0                
            assert(c1 or c2 or c3)

    # Compute result of veto protocol from commitments     
    B = functools.reduce(lambda a,b : a*b, [e[j] for e in b],1)
    print("\nB = ", B)
                  
    if v[j] == 1:
        print("\nVeto!")
        j_backarrow = j
        assert(B != 1) # This check may fail with low probability
    else:
        # Check if B is equal to 1 (g**0) when there is no veto
        assert(B == 1)

show("p = ", p)
show("d = ", d)
show("v = ", v)

# Check if result of the veto protocol is correct assuming p is available
assert(max(map(lambda e: int("".join(str(i) for i in e),2), p)) == int("".join(str(i) for i in v),2))
