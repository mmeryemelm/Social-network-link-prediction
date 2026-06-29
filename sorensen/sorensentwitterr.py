import networkx as nx
import matplotlib.pyplot as plt
from tabulate import tabulate
def common_in_neighbors(graph, node):
    return set(graph.predecessors(node))

def common_out_neighbors(graph, node):
    return set(graph.successors(node))

def sorensen_coefficient(graph, node1, node2):
    out_neighbors_node1 = common_out_neighbors(graph, node1)
    in_neighbors_node2 = common_in_neighbors(graph, node2)
    intersection = out_neighbors_node1.intersection(in_neighbors_node2)
    numerator = len(intersection)
    out_degree_x = graph.out_degree(node1)
    in_degree_y = graph.in_degree(node2)

    denominator = out_degree_x + in_degree_y

    if denominator == 0:
        return 0

    coefficient = (2 * numerator) / denominator
    return coefficient




def get_predicted_edges(graph, node):
    predicted_edges = []
    for neighbor in graph.nodes():
        if neighbor != node and not graph.has_edge(node, neighbor):
            coefficient = sorensen_coefficient(graph, node, neighbor)
            if coefficient > 0.2:  # Modify the threshold as desired
                predicted_edges.append((node, neighbor, coefficient))
    return predicted_edges

def plot_subgraph(graph, node, predicted_edges):
    plt.figure(figsize=(10, 6))
    pos = nx.random_layout(graph)

    # Create a subgraph with the selected node and its links
    subgraph = graph.subgraph([node] + [neighbor for _, neighbor, _ in predicted_edges])

    # Get the existing edges going from or into the selected node
    existing_edges = [(u, v) for u, v in graph.edges() if v == node or u == node]

    # Plot the subgraph with existing edges in black
    nx.draw_networkx_edges(subgraph, pos, edgelist=existing_edges, edge_color='black', width=1.0)

    # Plot the new predicted links in red
    nx.draw_networkx_edges(subgraph, pos, edgelist=predicted_edges, edge_color='red', width=1.0)

    nx.draw_networkx_nodes(subgraph, pos, node_color='lightblue', node_size=200)
    nx.draw_networkx_labels(subgraph, pos, font_size=8)

    plt.title(f'Sous-graphe du nœud {node} avec des liens existants et prédits')

    plt.show()


G = nx.DiGraph()

with open(r'C:\Users\DELL\Desktop\complexiteprjtfinal\soc-twitter-follows.mtx', 'r') as file:
    next(file)  # Skip the first line
    next(file)  # Skip the second line
    for line in file:
        numbers = list(map(int, line.split()))
        G.add_edge(numbers[0], numbers[1])

# Convert node labels to integers
G_int = nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute='old_label')

while True:
    # Select a specific node
    node = int(input("Entrez le numéro du nœud pour générer le tableau des liens prédits : "))

    if node not in G_int:
        print("Nœud invalide. Veuillez entrer un numéro de nœud valide.")
        continue

    # Get the predicted edges for the selected node
    predicted_edges = get_predicted_edges(G_int, node)

    if len(predicted_edges) == 0:
        print("Aucun lien prédit pour le nœud spécifié.")
    else:
        # Generate the table with the predicted edges and coefficient
        table_data = []
        for edge in predicted_edges:
            node1, node2, coefficient = edge
            table_data.append([node1, node2, coefficient])

        table = tabulate(table_data, headers=['Node 1', 'Node 2', 'Sørensen coefficient'], tablefmt='psql')
        print(table)

        # Create a subgraph with the selected node and predicted edges
        plot_subgraph(G_int, node, predicted_edges)

    choice = input("Souhaitez-vous entrer un autre nœud ?  (y/n): ")
    if choice.lower() != 'y':
        break
