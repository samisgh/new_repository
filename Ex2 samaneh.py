import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import copy


# reading the input file and define Undirected graph
graph = nx.Graph()
x = pd.read_csv('names.txt', sep=' ', header=None)
data = x.values
# to delete first column that is time
dataFiltered = np.delete(data, 0, axis=1)
graph.add_edges_from(dataFiltered)
numNode = graph.number_of_nodes()


# *********** Starting parameters *********

activePercentageThreshold = 70   # value used to choose if a node is active or not [1,100]
numNeighboor = 0.5    # percentage of neighbors infected in order to decide if a node is infected either or not [0,1]
n = 10     # number of simulation


numberInactive = 0     # number of not infected nodes
activeNode = {}      # active nodes dictionary, used to modify the attributes of the graph
# Activate node by using initial parameters
for i in list(graph.nodes):
    # select a random number between 0 ,100 to compare with the initial threshold for activate node
    x = random.randint(0, 100)
    if x < activePercentageThreshold:
        activeNode[i] = {'active': 0}
        # increasing the number of not Inactive nodes
        numberInactive += 1
    else:
        activeNode[i] = {'active': 1}

# setting the active nodes by using as attribute the created dictionary
nx.set_node_attributes(graph, activeNode)
# percentage of survived nodes at time 0
survivedNodes = numberInactive / numNode

inactiveNodeList = []
inactiveNodeList.append(survivedNodes)
# making a copy of the graph to check the situation of the nodes before changing its environment
oldGraph = copy.deepcopy(graph)
# making the simulation run for n times
for i in range(n):
    for j in list(graph.nodes):
        if graph.nodes[j]['active'] == 0:
            numberActiveNeighbors = 0
            for k in list(oldGraph.adj[j]):
                if oldGraph.nodes[k]['active'] == 1:
                    numberActiveNeighbors += 1
            numberActiveNeighbors = numberActiveNeighbors / len(list(oldGraph.adj[j]))
            if numberActiveNeighbors > numNeighboor:
                # set node j as active
                graph.nodes[j]['active'] = 1

    oldGraph = copy.deepcopy(graph)
    numberInactive = 0
    # counting the counter
    for z in list(graph.nodes):
        if graph.nodes[z]['active'] == 0:
            numberInactive += 1
    # fraction of survived nodes
    newSurvivedNodes = numberInactive / numNode
    inactiveNodeList.append(newSurvivedNodes)

print("Initial percentage of survived nodes:", round(survivedNodes, 3))
print("Final percentage of survived nodes:", round(newSurvivedNodes, 3))

# plotting the survived nodes in times
plt.figure()
plt.plot(inactiveNodeList)
plt.xlabel('time')
plt.ylabel('inactive nodes')
plt.title('proportion survival function (Inactive nodes)')
plt.show()
