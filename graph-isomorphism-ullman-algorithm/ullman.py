# zadanie ukonczone

import numpy as np

class Vertex:
    def __init__(self, xpos, ypos, key):
        self.key = key
        self.x = xpos
        self.y = ypos

    def __eq__(self, other):
        if isinstance(other, str):
            return self.key == other
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return f"{self.key} : x = {self.x}, y = {self.y}"

class Graph:

    def __init__(self):
        self.dct = {}
        self.lst = []
        self.tab = [[0]]
        self._size = 0

    def print_tab(self):
        for row in self.tab:
            print(row)

    def print_tab_format(self):
        for row in self.tab:
            print([edge for edge in row])

    def printGraph(self):
        n = self.order()
        print("------GRAPH------",n)
        for i in range(n):
            v = self.getVertex(i)
            print(v, end = " -> ")
            nbrs = self.neighbours(i)
            for vertex in nbrs:
                print(self.getVertex(vertex), self.tab[i][vertex].weight, end=";")
            print()
        print("-------------------")

    def insertVertex(self, vertex:Vertex):
        if self._size >= len(self.tab):
            self.expand()
        
        self.dct[vertex] = self._size
        self.lst.append(vertex)
        self._size += 1
        return self

    def expand(self):
        for row in self.tab:
            row.append(0)
        self.tab.append([0 for _ in range(len(self.tab[0]))])
        return self

    def insertEdge(self, vertex1, vertex2):
        if vertex1 not in self.lst:
            self.insertVertex(vertex1)
        if vertex2 not in self.lst:
            self.insertVertex(vertex2)
        self.tab[self.dct[vertex1]][self.dct[vertex2]] = 1
        self.tab[self.dct[vertex2]][self.dct[vertex1]] = 1
        return self

    def deleteEdge(self, vertex1, vertex2):
        self.tab[self.dct[vertex1]][self.dct[vertex2]] = 0
        self.tab[self.dct[vertex2]][self.dct[vertex1]] = 0
        return self

    def deleteVertex(self, vertex):
        del_index = self.dct[vertex]
        self.dct.pop(vertex)

        self.tab.pop(del_index)
        for row in self.tab:
            row.pop(del_index)
        
        self.lst.pop(del_index)

        for vertex in self.dct.keys():
            if self.dct[vertex] > del_index:
                self.dct[vertex] -= 1

        self._size -= 1
        return self

    def getVertexIdx(self, vertex):
        return self.dct[vertex]

    def getVertex(self, vertex_idx):
        return self.lst[vertex_idx]

    def neighbours(self, vertex_idx):
        neighs = []
        for i in range(len(self.tab)):
            if self.tab[vertex_idx][i] == 1:
                neighs.append(i)
        return neighs

    def order(self):
        return self._size

    def size(self):
        suma = 0
        for i in range(len(self.tab)):
            for j in range(i):
                if self.tab[i][j] != 0:
                    suma += 1
        return int(suma/2)

    def edges(self):
        full_edge_list = []

        for i in range(len(self.tab)):
            for j in range(i):
                if self.tab[i][j] == 1:
                    full_edge_list.append((self.lst[i].key, self.lst[j].key))
        compressed_list = []

        for pair in full_edge_list:
            inv_pair = (pair[1], pair[0])
            if pair not in compressed_list and inv_pair not in compressed_list:
                compressed_list.append(pair)
        return compressed_list


def prepare_M0(G,P):
    x = P.order()
    y = G.order()

    mtx = np.zeros((x,y))

    for u in range(mtx.shape[0]):
        dvu = sum(P.tab[u])
        for v in range(mtx.shape[1]):
            dvv = sum(G.tab[v])

            if dvu <= dvv:
                mtx[u][v] = 1
    return mtx


def Ullman_basic(used_cols, current_row, G, P, M):
    isomorphisms = 0
    recursions = 0
    
    recursions += 1

    if current_row == M.shape[0]:
        if np.array_equal(P, M @ (M @ G).T):
            isomorphisms += 1
            return isomorphisms, recursions
        return isomorphisms, recursions
    
    new_M = np.copy(M)

    t = 0
    for c in used_cols:
        if c == 0:
            new_M[current_row] = [0 for _ in range(M.shape[1])]
            new_M[current_row, t] = 1

            used_cols[t] = 1

            iso, rec = Ullman_basic(used_cols, current_row+1, G, P, new_M)

            isomorphisms += iso
            recursions += rec
            used_cols[t] = 0
        t += 1
    
    return isomorphisms, recursions


def test_Ullman_basic():
    graph_G = [('A','B',1), ('B','F',1), ('B','C',1), ('C','D',1), ('C','E',1), ('D','E',1)]
    G = Graph()
    for el in graph_G:
        G.insertEdge(el[0],el[1])

    graph_P = [('A','B',1), ('B','C',1), ('A','C',1)]
    P = Graph()
    for el in graph_P:
        P.insertEdge(el[0],el[1])

    G_tab = np.array(G.tab)
    P_tab = np.array(P.tab)
    M = np.zeros((P.order(), G.order()))

    print(Ullman_basic(np.zeros(G.order(), dtype=int), 0, G_tab, P_tab, M))
    return

def Ullman_M0(used_cols, current_row, G, P, M, M0):
    isomorphisms = 0
    recursions = 0

    recursions += 1

    if current_row == M.shape[0]:
        if np.array_equal(P, M @ (M @ G).T):
            isomorphisms += 1
            return isomorphisms, recursions
        return isomorphisms, recursions
    
    new_M = np.copy(M)

    t = 0
    for c in used_cols:
        if c == 0 and M0[current_row][t] == 1:
            new_M[current_row] = [0 for _ in range(M.shape[1])]
            new_M[current_row][t] = 1
            
            used_cols[t] = 1

            iso, rec = Ullman_M0(used_cols, current_row+1, G, P, new_M, M0)

            isomorphisms += iso
            recursions += rec
            used_cols[t] = 0
        t += 1
    
    return isomorphisms, recursions


def test_Ullman_M0():
    graph_G = [('A','B',1), ('B','F',1), ('B','C',1), ('C','D',1), ('C','E',1), ('D','E',1)]
    G = Graph()
    for el in graph_G:
        G.insertEdge(el[0],el[1])

    graph_P = [('A','B',1), ('B','C',1), ('A','C',1)]
    P = Graph()
    for el in graph_P:
        P.insertEdge(el[0],el[1])

    G_tab = np.array(G.tab)
    P_tab = np.array(P.tab)
    M = np.zeros((P.order(), G.order()))
    M0 = prepare_M0(G, P)

    print(Ullman_M0(np.zeros(G.order(), dtype=int), 0, G_tab, P_tab, M, M0))
    return


def prune(M, G, P):
    run = True
    while run:
        run = False
        for v in range(M.shape[1]):
            for u in range(M.shape[0]):
                if M[u][v] != 0:
                    for k in range(P.shape[0]):
                        if P[u][k] != 0:
                            for t in range(G.shape[0]):
                                if M[k][t] != 0:
                                    if G[v][t] == 0:
                                        M[u][v] = 0
                                        run = True



def Ullman_prune(used_cols, current_row, G, P, M, M0):
    isomorphisms = 0
    recursions = 0

    recursions += 1

    if current_row == M.shape[0]:
        if np.array_equal(P, M @ (M @ G).T):
            isomorphisms += 1
            return isomorphisms, recursions
        return isomorphisms, recursions

    new_M = np.copy(M)

    prune(M,G,P)
    for row in new_M[:current_row]:
        if (row==0).all():
            return isomorphisms, recursions

    t = 0
    for c in used_cols:
        if c == 0 and M0[current_row][t] == 1:
            new_M[current_row] = [0 for _ in range(M.shape[1])]
            new_M[current_row][t] = 1
            
            used_cols[t] = 1

            iso, rec = Ullman_prune(used_cols, current_row+1, G, P, new_M, M0)

            isomorphisms += iso
            recursions += rec

            used_cols[t] = 0
        t += 1
    
    return isomorphisms, recursions


def test_Ullman_prune():
    graph_G = [('A','B',1), ('B','F',1), ('B','C',1), ('C','D',1), ('C','E',1), ('D','E',1)]
    G = Graph()
    for el in graph_G:
        G.insertEdge(el[0],el[1])

    graph_P = [('A','B',1), ('B','C',1), ('A','C',1)]
    P = Graph()
    for el in graph_P:
        P.insertEdge(el[0],el[1])

    G_tab = np.array(G.tab)
    P_tab = np.array(P.tab)
    M = np.zeros((P.order(), G.order()))
    M0 = prepare_M0(G, P)

    print(Ullman_prune(np.zeros(G.order(), dtype=int), 0, G_tab, P_tab, M, M0))
    return

"""
--------------
Test functions
--------------
"""

test_Ullman_basic()
test_Ullman_M0()
test_Ullman_prune()