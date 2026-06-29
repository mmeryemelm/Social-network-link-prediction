import networkx as nx
from sklearn.metrics import roc_auc_score


def resource_allocation_index_directed(graph, node1, node2):
    out_neighbors1 = set(graph.successors(node1))
    in_neighbors2 = set(graph.predecessors(node2))
    common_neighbors = out_neighbors1.intersection(in_neighbors2)

    index = 0
    for common_node in common_neighbors:
        out_degree = graph.out_degree(common_node)
        if out_degree > 0:
            index += 1 / out_degree+1

    return index


G = nx.DiGraph()


with open(r'C:\Users\DELL\Desktop\complexiteprjtfinal\soc-google-plus.txt', 'r') as file:
    for line in file:
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

# Calculate maximum index for normalization
max_index = max(resource_allocation_index_directed(G, node1, node2) for (node1, node2) in test_edges)

# Calculate normalized indices
normalized_indices = [
    resource_allocation_index_directed(G, node1, node2) / max_index if max_index > 0 else 0
    for (node1, node2) in test_edges
]

# Méthode de prédiction basée sur le nombre de voisins communs
method = 'resource_allocation_index_directed'
auc = roc_auc_score([1] * len(positive_edges) + [0] * len(negative_edges), normalized_indices)

print(f"{method}: AUC = {auc}")
