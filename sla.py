import networkx as nx
from networkx.algorithms import node_classification
import numpy as np


def custom_harmonic_function(G):
    labels = {node: {} for node in G.nodes()}

    for node in G.nodes():
        if "label" in G.nodes[node]:
            labels[node][G.nodes[node]["label"]] = 1.0

    for _ in range(10):  # Número de iterações, ajuste conforme necessário
        new_labels = {node: {} for node in G.nodes()}

        for node in G.nodes():
            if "label" in G.nodes[node]:
                continue

            weighted_counts = {}

            for neighbor in G.neighbors(node):
                if "label" in G.nodes[neighbor]:
                    for label, data in G[node][neighbor].items():
                        weight = data.get("weight", 1.0)  # Acessar o atributo de peso
                        if label not in weighted_counts:
                            weighted_counts[label] = 0.0
                        weighted_counts[label] += weight * labels[neighbor][label]

            max_label = max(weighted_counts, key=weighted_counts.get)
            new_labels[node][max_label] = weighted_counts[max_label]

        labels = new_labels

    return labels


# Criar um grafo
G = nx.Graph()

# Adicionar nós e arestas com pesos
G.add_edge(0, 1, weight=0.5)
G.add_edge(0, 2, weight=0.2)
G.add_edge(1, 2, weight=0.7)
G.add_edge(2, 3, weight=0.4)

# Definir rótulos iniciais para alguns nósd
G.nodes[0]["label"] = "A"
G.nodes[3]["label"] = "B"

predicted_labels = custom_harmonic_function(G)
print(predicted_labels)
