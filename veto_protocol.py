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

# Bids by party by bits            
p = [[0,1,0,1,0],
     [0,1,0,0,1],
     [0,0,1,1,1]]

n = len(p)
m = len(p[0])

# Declared bids by party by bits
d = [[0 for j in range(m)] for i in range(n)]

# Veto per round
v = [0 for i in range(m)]

# Index of last veto
j_star = -1

# Veto protocol
for j in range(m):
    print("\nRound " + str(j))
    print("j_star = " + str(j_star))
    for i in range(n):
        
        if j_star == -1:
            d[i][j] = 1 if p[i][j] == 1 else 0
        else:
            d[i][j] = 1 if p[i][j] and d[i][j_star] == 1 else 0
            
        print("Party " + str(i) + " : p = " + str(p[i][j]) + " d* = " + str(d[i][j_star]) + " d = " + str(d[i][j]))
                    
        v[j] = 1 if v[j] or d[i][j] == 1 else 0
        
        # Check logical conditions guaranteeing that parties are following the protocol
        if j_star == -1:
            # c0 must hold until first veto
            c0 = p[i][j] == d[i][j]
            assert(c0)
        else:            
            # c1 or c2 or c3 must hold after first veto
            c1 = p[i][j] == 0 and d[i][j] == 0
            c2 = p[i][j] == 1 and d[i][j_star] == 1 and d[i][j] == 1
            c3 = d[i][j_star] == 0 and d[i][j] == 0                
            assert(c1 or c2 or c3)
        
    if v[j] == 1:
        print("\nVeto!")
        j_star = j     

show("p = ", p)
show("d = ", d)
show("v = ", v)
