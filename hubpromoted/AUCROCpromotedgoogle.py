import networkx as nx
from sklearn.metrics import roc_auc_score



def hub_promoted(graph, node1, node2):
    out_neighbors = set(graph.successors(node1))
    in_neighbors = set(graph.predecessors(node2))
    common_neighbors = out_neighbors.intersection(in_neighbors)
    min_degree = min(graph.out_degree(node1), graph.in_degree(node2))
    if min_degree == 0:
        return 0
    hub_promotion = len(common_neighbors) / min_degree
    return hub_promotion

G = nx.DiGraph()

with open(r'C:\Users\DELL\Desktop\complexiteprjtfinal\soc-google-plus.txt', 'r') as file:
    for line in file:
        numbers = list(map(int, line.split()))
        G.add_edges_from([(numbers[0], numbers[1])])

# Convert node labels to integers
G_int = nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute='old_label')


positive_edges = []
negative_edges = []

for node1 in G.nodes():
    successors = list(G.successors(node1))
    if successors:
        node2 = successors[0]
        positive_edges.append((node1, node2))
    else:
        negative_edges.append((node1, node2))



test_edges = positive_edges + negative_edges



method = 'hub_promoted'
auc = roc_auc_score([1] * len(positive_edges) + [0] * len(negative_edges),
                    [hub_promoted(G, node1, node2) for (node1, node2) in test_edges])

print(f"{method}: AUC = {auc}")
