import networkx as nx
from sklearn.metrics import roc_auc_score
import math


def adamic_adar_index(graph, node1, node2):
    out_neighbors1 = set(graph.successors(node1))
    out_neighbors2 = set(graph.successors(node2))
    common_out_neighbors = out_neighbors1.intersection(out_neighbors2)

    index = 0
    for neighbor in common_out_neighbors:
        out_degree = graph.out_degree(neighbor)
        if out_degree > 0:
            index += 1 / math.log(out_degree+1)
    return index


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

# Calculate the true labels for the test edges
true_labels = [1] * len(positive_edges) + [0] * len(negative_edges)

# Calculate the predicted scores for the test edges using the adamic_adar_index
predicted_scores = []
for node1, node2 in test_edges:
    score = adamic_adar_index(G, node1, node2)
    if math.isfinite(score):
        predicted_scores.append(score)
    else:
        predicted_scores.append(0)

# Calculate the AUC score
auc = roc_auc_score(true_labels, predicted_scores)

print(f"adamic_adar_index: AUC = {auc}")
