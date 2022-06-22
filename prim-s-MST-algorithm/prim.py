#zadanie ukonczone

import numpy as np
import copy


class Vertex:
    def __init__(self, key):
        self.key = key
        # self.xpos = xpos
        # self.ypos = ypos

    def __eq__(self, other):
        if isinstance(other, str):
            return self.key == other
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return f"{self.key}"

class Edge:
    def __init__(self, start, end, weight):
        self.start = start
        self.end = end
        self.weight = weight

class Graph:

    def __init__(self):
        self.dct = {}
        self.lst = []
        self.tab = [[None]]
        self._size = 0

    def print_tab(self):
        for row in self.tab:
            print(row)

    def print_tab_format(self):
        for row in self.tab:
            print([str(edge.weight)+" " if isinstance(edge, Edge) else str(edge) for edge in row])

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
            row.append(None)
        self.tab.append([None for _ in range(len(self.tab[0]))])
        return self

    def insertEdge(self, vertex1, vertex2, edge):
        if vertex1 not in self.lst:
            self.insertVertex(vertex1)
        if vertex2 not in self.lst:
            self.insertVertex(vertex2)
        self.tab[self.dct[vertex1]][self.dct[vertex2]] = edge
        self.tab[self.dct[vertex2]][self.dct[vertex1]] = edge
        return self

    def deleteEdge(self, vertex1, vertex2):
        self.tab[self.dct[vertex1]][self.dct[vertex2]] = None
        self.tab[self.dct[vertex2]][self.dct[vertex1]] = None
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

    # def blockVertex(self, vertex):  # used in Prim's MST construction algorithm
    #     block_index = self.dct[vertex]    # not used at all :)
    #     for i in range(len(self.tab)):
    #         self.tab[i][block_index] = None
    #     return self


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


def MST_Prim(G:Graph, s:Vertex):
    intree = [0 for _ in range(len(G.lst))]
    distance = [np.inf for _ in range(len(G.lst))]
    parent = [-1 for _ in range(len(G.lst))]
    tree_length = 0

    MST = Graph()   # initialize empty structure for MST - subgraph
    for vertex in G.lst:
        MST.insertVertex(vertex)

    v = MST.dct[s]  # indeks rozważanego wierzchołka

    while intree[v] == 0:   # dopóki rozważany wierzchołek jest poza drzewem
        intree[v] = 1   # dodajemy rozważany wierzchołek do drzewa

        for edge in G.tab[v]:   # przeglądamy otoczenie wierzchołka
            if edge:    # jeżeli istnieje krawędź z wierzchołka v
                if intree[G.dct[edge.end]] == 0:    # jeżeli wierzchołek nie jest w drzewie
                    if edge.weight < distance[v]:   #   jeżeli koszt dotarcia jest mniejszy niż aktualny w tablicy
                        distance[v] = edge.weight   # uaktualniamy distance
                        parent[v] = edge.end    # zapamiętujemy poprzednika
        
        h_distance = np.inf
        h_vertex = None

        for vertex in MST.lst:  # przegląd każdego wierzchołka w grafie
            if intree[G.dct[vertex]] == 0:  # ograniczenie przeglądu tylko do wierzchołków niebędących w drzewie
                if G.tab[v][G.dct[vertex]]:
                    if G.tab[v][G.dct[vertex]].weight < h_distance:  # szukamy najtańszej krawędzi
                        h_distance = G.tab[v][G.dct[vertex]].weight
                        h_vertex = vertex
        
        
        if h_vertex:
            MST.insertEdge(G.lst[v], h_vertex, Edge(G.lst[v], h_vertex, h_distance))  # dodajemy krawędź w obie strony
            MST.insertEdge(h_vertex, G.lst[v], Edge(h_vertex, G.lst[v], h_distance))
            tree_length += h_distance
        else:
            break
        v = G.dct[h_vertex]    # obieramy nowo przyłączony wierzchołek jako aktualny

    return MST, tree_length




def test1():
    G = Graph()
    graf = [ ('A','B',4), ('A','C',1), ('A','D',4),
         ('B','E',9), ('B','F',9), ('B','G',7), ('B','C',5),
         ('C','G',9), ('C','D',3),
         ('D', 'G', 10), ('E', 'H', 4),('E', 'I', 6), ('D', 'J', 18),
         ('E', 'F', 2),
         ('F', 'H', 2), ('F', 'G', 8),
         ('G', 'H', 9), ('G', 'J', 8),
         ('H', 'I', 3), ('H','J',9),
         ('I', 'J', 9)
        ]
    for (a,b,weight) in graf:
        G.insertEdge(Vertex(a),Vertex(b),Edge(Vertex(a),Vertex(b),weight))

    MST, length = MST_Prim(G, G.lst[0])
    # MST.print_tab_format()
    MST.printGraph()
    
    
test1()


