import networkx as nx
from sklearn.metrics import roc_auc_score




def hub_depressed(graph, node1, node2):
    out_neighbors = set(graph.successors(node1))
    in_neighbors = set(graph.predecessors(node2))
    common_neighbors = out_neighbors.intersection(in_neighbors)
    max_degree = max(graph.out_degree(node1), graph.in_degree(node2))
    if max_degree == 0:
        return 0
    hub_depressed = len(common_neighbors) / max_degree
    return hub_depressed

G = nx.DiGraph()

with open(r'C:\Users\DELL\Desktop\complexiteprjtfinal\Wiki-Vote.txt', 'r') as file:
    for line in file:
        if line.startswith('#'):
            continue
        numbers = list(map(int, line.split()))
        G.add_edges_from([(numbers[0], numbers[1])])

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
method = 'hub_depressed'
auc = roc_auc_score([1] * len(positive_edges) + [0] * len(negative_edges),
                    [hub_depressed(G, node1, node2) for (node1, node2) in test_edges])

print(f"{method}: AUC = {auc}")
