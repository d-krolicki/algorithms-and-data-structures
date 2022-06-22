# zadanie ukonczone

import numpy as np


"""
Graph data structure adaptation for max-flow problem.
"""

class Vertex:
    def __init__(self, key):
        self.key = key

    def __eq__(self, other):
        if isinstance(other, str):
            return self.key == other
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return f"{self.key}"

class Edge:
    def __init__(self, start, end, capacity, isResidual = False):
        self.start = start
        self.end = end
        self.capacity = capacity
        self.isResidual = isResidual
        if isResidual:
            self.residual = 0
            self.flow = 0
        else:
            self.residual = self.capacity
            self.flow = 0

    def __repr__(self):
        return f"{self.capacity} {self.flow} {self.residual} {self.isResidual}"

class FlowGraph:

    def __init__(self):
        self.dct = {}
        self.lst = []
        self.tab = [[None]]
        self.res_tab = [[None]]
        self._size = 0

    def print_tab(self):
        for row in self.tab:
            print(row)
        for row in self.res_tab:
            print(row)

    def print_tab_format(self):
        for row in self.tab:
            print([f"{edge.flow}/{edge.capacity}"+" " if isinstance(edge, Edge) else str(edge) for edge in row])
        print()
        for row in self.res_tab:
            print([f"{edge.flow}/{edge.residual}"+" " if isinstance(edge, Edge) else str(edge) for edge in row])

    def printGraph(self):
        n = self.order()
        print("------REAL PART------",n)
        for i in range(n):
            v = self.getVertex(i)
            print(v, end = " -> ")
            nbrs = self.neighbours(i)
            for vertex in nbrs:
                print(self.getVertex(vertex), f"{self.tab[i][vertex].flow}/{self.tab[i][vertex].capacity}", end=";")
            print()
        print("-------------------")

        print("------RESIDUAL PART------",n)
        for i in range(n):
            v = self.getVertex(i)
            print(v, end = " -> ")
            nbrs = self.res_neighbours(i)
            for vertex in nbrs:
                print(self.getVertex(vertex), f"{self.res_tab[i][vertex].flow}/{self.res_tab[i][vertex].residual}", end=";")
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
            row.append(None)
        self.tab.append([None for _ in range(len(self.tab[0]))])

        for row in self.res_tab:
            row.append(None)
        self.res_tab.append([None for _ in range(len(self.res_tab[0]))])
        return self

    def insertEdge(self, vertex1, vertex2, edge):
        if vertex1 not in self.lst:
            self.insertVertex(vertex1)
        if vertex2 not in self.lst:
            self.insertVertex(vertex2)
        if edge.isResidual:
            self.insertResidualEdge(vertex1, vertex2, edge)
            return self
        self.tab[self.dct[vertex1]][self.dct[vertex2]] = edge
        self.res_tab[self.dct[vertex2]][self.dct[vertex1]] = Edge(edge.start, edge.end, edge.capacity, isResidual=True)

        return self

    def deleteEdge(self, vertex1, vertex2):
        self.tab[self.dct[vertex1]][self.dct[vertex2]] = None
        self.res_tab[self.dct[vertex2]][self.dct[vertex1]] = None   
        return self

    def deleteVertex(self, vertex):
        del_index = self.dct[vertex]
        self.dct.pop(vertex)

        self.tab.pop(del_index)
        for row in self.tab:
            row.pop(del_index)
        self.res_tab.pop(del_index)
        for row in self.res_tab:
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
            if self.tab[vertex_idx][i]:
                neighs.append(i)
        return neighs

    def res_neighbours(self, vertex_idx):
        neighs = []
        for i in range(len(self.res_tab)):
            if self.res_tab[vertex_idx][i]:
                neighs.append(i)
        return neighs

    def order(self):
        return self._size

    def size(self):
        suma = 0
        for i in range(len(self.tab)):
            for j in range(i):
                if self.tab[i][j] != None:
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

"""
BFS Algorithm.
"""

def BFS_traversal(G:FlowGraph, s:Vertex):
    visited = [False for _ in range(len(G.lst))]
    parent = [None for _ in range(len(G.lst))]
    queue = []

    queue.append(s)
    visited[G.dct[s]] = True

    while queue:
        current = queue.pop()
        neighbours = G.neighbours(G.dct[current])

        for vertex in neighbours:
            if not visited[G.dct[G.lst[vertex]]]:
                if G.tab[G.dct[current]][G.dct[G.lst[vertex]]].residual > 0:
                    queue.append(G.lst[vertex])
                    visited[G.dct[G.lst[vertex]]] = True
                    parent[G.dct[G.lst[vertex]]] = current
    return parent

"""
Minimal capacity computation.
"""

def compute_min_capacity(G:FlowGraph, parent, start, end):
    current_vertex = end
    min_capacity = np.inf

    if parent[G.dct[end]] is None:
        return 0
    
    while current_vertex != start:
        par = parent[G.dct[current_vertex]]
        if min_capacity > G.tab[G.dct[par]][G.dct[current_vertex]].residual:
            min_capacity = G.tab[G.dct[par]][G.dct[current_vertex]].residual

        current_vertex = par
    
    return min_capacity

"""
Augment path.
"""
def augment(G:FlowGraph, start, end, parent, min_capacity):
    current_vertex = end

    while current_vertex != start:
        par = parent[G.dct[current_vertex]]
        G.tab[G.dct[par]][G.dct[current_vertex]].flow += min_capacity
        G.tab[G.dct[par]][G.dct[current_vertex]].residual -= min_capacity

        G.res_tab[G.dct[current_vertex]][G.dct[par]].residual += min_capacity

        current_vertex = par
    return


"""
Ford-Fulkerson algorithm.
"""

def FordFulkerson(G:FlowGraph):
    start = Vertex('s')
    end = Vertex('t')

    parent = BFS_traversal(G, Vertex('s'))
    min_capacity = compute_min_capacity(G, parent, start, end)
    

    while min_capacity > 0:
        augment(G, start, end, parent, min_capacity)
        parent = BFS_traversal(G, Vertex('s'))
        min_capacity = compute_min_capacity(G, parent, start, end)
    
    child_index = G.dct[Vertex('t')]
    nb_edges = []
    for i in range(len(G.lst)):
        if type(G.tab[i][child_index]) == Edge:
            nb_edges.append(G.tab[i][child_index])
    
    sum = 0
    for edge in nb_edges:
        sum += edge.flow


    return sum


"""
Test case.
"""

def test0():

    G = FlowGraph()
    graf_0 = [ ('s','u',2), ('u','t',1), ('u','v',3), ('s','v',1), ('v','t',2)]
    for (start, end, capacity) in graf_0:
        G.insertEdge(Vertex(start), Vertex(end), Edge(Vertex(start), Vertex(end), capacity))
    

    return FordFulkerson(G), G

"""
Test case.
"""
def test1():

    G = FlowGraph()
    graf_1 = [ ('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9), ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4) ]
    for (start, end, capacity) in graf_1:
        G.insertEdge(Vertex(start), Vertex(end), Edge(Vertex(start), Vertex(end), capacity))
    
    return FordFulkerson(G), G

"""
Test case.
"""
def test2():

    G = FlowGraph()
    graf_2 = [ ('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6), ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    for (start, end, capacity) in graf_2:
        G.insertEdge(Vertex(start), Vertex(end), Edge(Vertex(start), Vertex(end), capacity))
    
    return FordFulkerson(G), G

"""
Test case.
"""
def test3():

    G = FlowGraph()
    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7), ('d', 'c', 4)]
    for (start, end, capacity) in graf_3:
        G.insertEdge(Vertex(start), Vertex(end), Edge(Vertex(start), Vertex(end), capacity))
    
    return FordFulkerson(G), G

"""
Test case activations.
"""


print(f"Maximum flow for graph 0 is {test0()[0]}. The graph looks like below.")
test0()[1].printGraph()
print(f"Maximum flow for graph 1 is {test1()[0]}. The graph looks like below.")
test1()[1].printGraph()
print(f"Maximum flow for graph 2 is {test2()[0]}. The graph looks like below.")
test2()[1].printGraph()
print(f"Maximum flow for graph 3 is {test3()[0]}. The graph looks like below.")
test3()[1].printGraph()