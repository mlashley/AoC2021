#!/usr/bin/python3
import networkx as nx
import matplotlib.pyplot as plt
import os

class Cave:
    def __init__(self, name):
        self.name = name
        self.isVisited = False
        self.isLarge = False
        if name.upper() == name:
            self.isLarge = True
        self.adjacents = []
    def __str__(self):
        return f"Cave[{self.name} L:{self.isLarge} V:{self.isVisited}]"
    def __repr__(self):
        return f"Cave[{self.name} L:{self.isLarge} V:{self.isVisited}]"
    def addAdjacent(self,cave):
        self.adjacents.append(cave)

def readNodes(fn):
    global G
    f = open(fn,"r")
    for line in f:
        print(f"Processing {line.strip()}")
        elems = [ x for x in line.strip().split('-')]
        for cave in elems:
            if cave in caves:
                print(f"Already exists - Not adding {cave}")
            else:
                caves[cave] = Cave(cave)
        caves[elems[0]].addAdjacent(caves[elems[1]])
        caves[elems[1]].addAdjacent(caves[elems[0]])
        G.add_edges_from([elems])
        
def walk(cave,invisited,twoferUsed):
    global pathCount
    visited = invisited.copy()
    print(f"Walking {cave} - been to {visited}")
    visited.append(cave.name)
    if cave.name == 'end':
        print(f"Reached End {visited}")
        pathCount = pathCount + 1
        nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size = 1500)
        nx.draw_networkx_labels(G, pos)
        redEdges = [ p for p in zip(visited[::1], visited[1::1]) ]
        blackEdges = [edge for edge in G.edges() if edge not in redEdges ]
        nx.draw_networkx_edges(G, pos, edgelist=redEdges, edge_color='r', arrows=True)
        nx.draw_networkx_edges(G, pos, edgelist=blackEdges, edge_color='black', arrows=False)
        # plt.show()
        plt.savefig(f"path{str(pathCount).zfill(5)}.png")
        plt.close()

        return visited
    for candidate in cave.adjacents:
        if (not candidate.isLarge) and (candidate.name in visited and not twoferUsed) and (candidate.name not in ["start","end"]):
            print(f"Visiting {candidate} using twofer")
            walk(candidate,visited,True) 
        elif candidate.isLarge or candidate.name not in visited: #
            print(f"Visiting {candidate} twofer: {twoferUsed}")
            walk(candidate,visited,twoferUsed)
    visited.pop()

# inputs = ["input.test","input.test2","input.test3","input"]
inputs = ["input.test"] # Suggest not running this for 90K frames of output ;-)
for filename in inputs:
    os.system("rm path*.png")
    G = nx.DiGraph()
    # Use a dict - so we don't need to care about dupes.
    caves = {}
    paths = {}
    pathCount = 0
    readNodes(filename)
    pos = nx.kamada_kawai_layout(G)
    values = [0.25 for node in G.nodes()]

    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size = 1500)
    nx.draw_networkx_labels(G, pos)

    # # Specify the edges you want here
    # red_edges = [('A', 'C'), ('E', 'C')]
    # edge_colours = ['black' if not edge in red_edges else 'red'
    #             for edge in G.edges()]
    # black_edges = [edge for edge in G.edges() if edge not in red_edges]

    nx.draw_networkx_edges(G, pos, edgelist=G.edges, arrows=True)
    # plt.show()
    walk(caves['start'],[],False)
    print(f"Found {pathCount} Paths in {filename}")
    os.system(f"ffmpeg -i path%05d.png {filename}.gif")