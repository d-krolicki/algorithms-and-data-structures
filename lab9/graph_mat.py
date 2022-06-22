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

class AdjMatrixApp:

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
