from typing import List, Dict, Tuple
from numpy import inf as INF
import copy

import polska


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
    def __init__(self, start, end, weight=0):
        self.start = start
        self.end = end
        self.weight = weight        

class AdjListApp:

    def __init__(self):
        self.dct = {}
        self.lst = []
        self.vertices = []
        self.vertexFromKey = {}

    def insertVertex(self, vertex):
        if isinstance(vertex, Vertex):
            self.vertices.append(vertex)
            self.dct[vertex] = len(self.vertices)-1
            self.vertexFromKey[vertex.key] = vertex
            self.lst.append([])
            return self
        else:
            print("Wystapil blad w trakcie wstawiania wierzcholka.")
            return None

    def insertEdge(self, edge):
        vertex1, vertex2 = edge.start, edge.end
        # print(f"vertex1: {vertex1}")
        # print(f"vertex2: {vertex2}")
        # print(f"dct[vertex1]: {self.dct[vertex1]}")
        # print(f"dct[vertex2]: {self.dct[vertex2]}")
        # print(f"self.lst: {self.lst}")
        self.lst[self.dct[vertex1]].append(self.dct[vertex2])
        # print("Edge inserted.")
        return self

    def deleteEdge(self, v1, v2):
        """ 
        Usuwanie krawedzi w obie strony, bo graf jest nieskierowany. 
        """
        try:
            self.lst[self.dct[v1]].remove(self.dct[v2])
            self.lst[self.dct[v2]].remove(self.dct[v1])
            return self
        except:
            print("Wystapil blad przy usuwaniu krawedzi - moze taka krawedz nie istnieje?")
            return None
    

    def deleteVertex(self, vertex):
        vert = copy.deepcopy(vertex)
        del_index = self.dct[vert]

        """ 
        Skopiuj informacje z konca listy na miejsce wczesniej, a nastepnie
        obetnij koniec listy.
        """
        self.vertices[del_index] = self.vertices[-1]
        self.vertices = self.vertices[:-1]

        self.dct.pop(vertex)  # Aktualizacja slownika - usuwanie wierzcholka

        """
        Aktualizacja indeksów w słowniku.
        """
        for vertex in self.dct:
            if self.dct[vertex] > del_index:
                self.dct[vertex] -= 1

        # lst_help = copy.deepcopy(self.lst)
        new_list = []
        for index, list in enumerate(self.lst):
            new_list.append([])
            for el in list:
                if el < del_index:
                    new_list[index].append(el)
                elif el > del_index:
                    new_list[index].append(el-1)
        
        self.lst = new_list
        self.lst.pop(del_index)
        return self
            

    def getVertexIdx(self, v):
        return self.dct[v]

    def getVertex(self, v_id):
        return self.vertices[v_id]

    def neighbours(self, v_id):
        return self.lst[v_id]
    
    def order(self):
        return len(self.vertices)

    def size(self):
        suma = 0
        for list in self.lst:
            suma += len(list)
        return int(suma/2)

    def edges(self):
        full_edge_list = []

        for index, list in enumerate(self.lst):
            for el in list:
                # print(f"index:{index}")
                # print(f"el:{el}")
                full_edge_list.append((self.vertices[index], self.vertices[el]))    

        compressed_list = []

        for pair in full_edge_list:
            inv_pair = (pair[1], pair[0])
            if pair not in compressed_list and inv_pair not in compressed_list:
                compressed_list.append(pair)
        return compressed_list


def test1():
    G = AdjListApp()

    for x,y,rej in polska.polska:
        G.insertVertex(Vertex(x,y,rej))
    
    for a,b in polska.graf:
        G.insertEdge(Edge(a,b))
    
    for v in G.lst:
        print(v)
    print(30*'-')
    G.deleteVertex("K")
    for v in G.lst:
        print(v)
    G.deleteEdge("W","E")

    polska.draw_map(G.edges())
test1()
