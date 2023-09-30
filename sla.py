import networkx as nx

# Criar um grafo direcionado ponderado
G = nx.DiGraph()

# Adicionar nós e arestas com pesos
G.add_edge("A", "B", weight=0.5)
G.add_edge("A", "C", weight=0.2)
G.add_edge("B", "C", weight=0.7)
G.add_edge("C", "D", weight=0.4)

# Inicializar as labels dos nós com valores iniciais
node_labels = {"A": 'L', "B": 'R', "C": 'R', "D": 'N'}

# Número de iterações para atualizar as labels
num_iteracoes = 10

for _ in range(num_iteracoes):
    new_labels = {}
    for node in G.nodes():
        weighted_label_sum = 0.0
        total_weight = 0.0

        for predecessor in G.predecessors(node):
            weight = G[predecessor][node].get("weight", 1.0)
            weighted_label_sum += weight * node_labels[predecessor]
            total_weight += weight

        if total_weight > 0:
            new_labels[node] = weighted_label_sum / total_weight
        else:
            new_labels[node] = node_labels[node]

    node_labels = new_labels

# Exibir as labels finais
for node, label in node_labels.items():
    print(f"{node}: {label}")
