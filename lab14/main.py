from re import L
import numpy as np

def string_compare_req(P:str, T:str, i:int, j:int):
    if i == 0:
        return
    if j==0:
        return
    swaps = string_compare_req(P, T, i-1, j-1) + int(P[i]!=T[j])
    insertions = string_compare_req(P, T, i, j-1) + 1
    deletions = string_compare_req(P, T, i-1, j) + 1

    smallest_cost = min([swaps, insertions, deletions])
    return smallest_cost

P = ' biały autobus'
T = ' czarny autokar'

# print(string_compare_req(P,T,2,2))


def string_compare_PD(P,T):
    m = len(P)
    n = len(T)
    D = np.zeros((m,n), dtype='int')
    Ps = np.full((m,n), "X", dtype='str')
    for i in range(m):
        D[i][0] = i
    for j in range(n):
        D[0][j] = j
    for i in range(1,m):
        for j in range(1,n):
            pass
            if P[i] == T[j]:
                D[i][j] = D[i-1, j-1]
            else:
                temp = [D[i, j-1], D[i-1,j], D[i-1,j-1]]
                min_ = min(temp)
                D[i][j] = min_+ 1
                op_idx = temp.index(min_)
                if op_idx == 0:
                    Ps[i][j] = "S"
                elif op_idx == 1:
                    Ps[i][j] = "I"
                elif op_idx == 2:
                    Ps[i][j] = "D"
    print(D)
    print(Ps)
    return D[m-1,n-1]

print(string_compare_PD(P,T))