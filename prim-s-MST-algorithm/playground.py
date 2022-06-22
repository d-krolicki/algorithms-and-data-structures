import numpy as np

lst = [3,5,None]
print(np.min(lst))


    # MST = Graph()   # initialize empty structure for MST - subgraph


    # MST.insertVertex(s) # starting vertex for MST
    # G.blockVertex(s)    # mark the vertex as included into MST

    # for _ in range(len(G.lst)-1):   # main loop - runs as many times as there are vertices in the graph
    #     try:
    #         min_cost_edge = Edge(Vertex('ERR'), Vertex('ERR'), np.inf)    # empty space for the edge to be joined into MST
    #         for vertex in MST.lst:  # iterate over all the vertices in MST - finding the next one in graph
    #             vertex_index = G.dct[vertex]
    #             for i in range(len(G.tab[vertex_index])):
    #                 if G.tab[vertex_index][i]:
    #                     if G.tab[vertex_index][i].weight < min_cost_edge.weight:
    #                         min_cost_edge = G.tab[vertex_index][i]  # minimal cost edge found
    #         MST.insertEdge(min_cost_edge.start, min_cost_edge.end, min_cost_edge.weight)
    #         G.blockVertex(min_cost_edge.end)
    #     except:
    #         return None
