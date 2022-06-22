import copy


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
    def __init__(self, start, end, capacity, isResidual=False):
        self.start = start
        self.end = end
        self.capacity = capacity
        self.isResidual = isResidual
        # self.flow = 0
        if self.isResidual:
            self.residual = 0
        if not self.isResidual:
            self.flow = 0
            self.residual = capacity
    
    def __repr__(self):
        return f"{self.capacity} {self.flow} {self.residual} {self.isResidual}"
        


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

    def insertEdge(self, vertex1, vertex2, edge=1):
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