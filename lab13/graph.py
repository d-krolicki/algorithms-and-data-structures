from typing import List, Dict, Tuple
from numpy import inf as INF
import copy


class Vertex:
    def __init__(self, xpos, ypos, key):
        self.key = key
        self.xpos = xpos
        self.ypos = ypos

    def __eq__(self, other):
        if isinstance(other, str):
            return self.key == other
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return f"{self.key}:({self.xpos},{self.ypos})"

class Edge:
    def __init__(self, start, end, weight):
        self.start = start
        self.end = end
        self.weight = weight

class AdjMatrixApp:

    def __init__(self):
        self.dct = {}
        self.lst = []
        self.tab = [[0]]
        self._size = 0

    def print_tab(self):
        for row in self.tab:
            print(row)

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

    def insertEdge(self, vertex1, vertex2, edge=1):
        self.tab[self.dct[vertex1]][self.dct[vertex2]] = edge
        self.tab[self.dct[vertex2]][self.dct[vertex1]] = edge
        return self

    def deleteEdge(self, vertex1, vertex2):
        self.tab[self.dct[vertex1]][self.dct[vertex2]] = 0
        self.tab[self.dct[vertex2]][self.dct[vertex1]] = 0
        return self

    def deleteVertex(self, vertex):
        del_index = self.dct[vertex]

        self.tab.pop(del_index)
        for row in self.tab:
            row.pop(del_index)
        
        self.lst.pop(del_index)

        for vertex in self.dct:
            if self.dct[vertex] > del_index:
                self.dct[vertex] -= 1

        self._size -= 1
        return self

    def getVertexIdx(self, vertex):
        return self.dct[vertex]

    def getVertex(self, vertex_idx):
        return self.lst[vertex_idx]

    def neighbours(self, vertex_idx):
        neighbours = []
        for i in range(len(self.tab)):
            if self.tab[vertex_idx][i] == 1:
                neighbours.append(i)
        return neighbours

    def order(self):
        return self._size

    def size(self):
        suma = 0
        for i in range(len(self.tab)):
            for j in range(i):
                if self.tab[i][j] == 1:
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
