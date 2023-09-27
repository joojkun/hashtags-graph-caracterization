from networkx.algorithms import node_classification
import networkx as nx

G = nx.path_graph(4)
G.nodes[0]["label"] = "A"
G.nodes[3]["label"] = "B"

predicted = node_classification.harmonic_function(G)
print(predicted)
# Saída: ['A', 'A', 'B', 'B']
