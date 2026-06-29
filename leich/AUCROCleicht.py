import networkx as nx
from sklearn.metrics import roc_auc_score




def leicht_holme_newman_index(graph, node1, node2):
    out_neighbors = set(graph.successors(node1))
    in_neighbors = set(graph.predecessors(node2))
    common_neighbors = out_neighbors.intersection(in_neighbors)
    out_degree = graph.out_degree(node1)
    in_degree = graph.in_degree(node2)
    if out_degree == 0 or in_degree == 0:
        return 0
    index = len(common_neighbors) / (out_degree * in_degree)
    return index


G = nx.DiGraph()

# Read the graph data from file
with open(r'C:\Users\DELL\Desktop\complexiteprjtfinal\soc-twitter-follows.mtx', 'r') as file:
    next(file)  # Skip the first line
    next(file)  # Skip the second line
    for line in file:
        numbers = list(map(int, line.split()))
        G.add_edge(numbers[0], numbers[1])

# Convert node labels to integers
G_int = nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute='old_label')

# Generate the list of positive and negative test edges
positive_edges = []
negative_edges = []
for node1 in G.nodes():
    successors = list(G.successors(node1))
    if successors:
        node2 = successors[0]
        positive_edges.append((node1, node2))
    else:
        negative_edges.append((node1, node2))

# Combine positive and negative edges
test_edges = positive_edges + negative_edges

# Méthode de prédiction basée sur le nombre de voisins communs
method = 'leicht_holme_newman_index'
auc = roc_auc_score([1] * len(positive_edges) + [0] * len(negative_edges),
                    [leicht_holme_newman_index(G, node1, node2) for (node1, node2) in test_edges])

print(f"{method}: AUC = {auc}")
