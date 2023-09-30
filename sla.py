import networkx as nx
from networkx.algorithms import node_classification

G = nx.path_graph(4)
G.nodes[0]["label"] = "A"
G.nodes[3]["label"] = "B"
G.nodes(data=True)
G.edges()
predicted = node_classification.harmonic_function(G)
print(predicted)
