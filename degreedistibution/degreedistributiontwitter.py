

import networkx as nx
import matplotlib.pyplot as plt

# Read the MTX file and create a directed graph
G = nx.DiGraph()
with open(r'C:\Users\DELL\Desktop\complexiteprjtfinal\soc-twitter-follows.mtx', 'r') as file:
    for line in file:
        if not line.startswith('%'):
            edge = line.strip().split()
            if len(edge) == 2:
                node1, node2 = edge
                G.add_edge(node1, node2)

# Calculate the in-degree distribution
in_degree_freq = [0] * (max(dict(G.in_degree()).values()) + 1)
for _, deg in G.in_degree():
    in_degree_freq[deg] += 1

# Calculate the out-degree distribution
out_degree_freq = [0] * (max(dict(G.out_degree()).values()) + 1)
for _, deg in G.out_degree():
    out_degree_freq[deg] += 1

# Plot the degree distributions
plt.figure(figsize=(12, 8))
plt.loglog(range(len(in_degree_freq)), in_degree_freq, 'go-', label='In-degree')
plt.loglog(range(len(out_degree_freq)), out_degree_freq, 'bo-', label='Out-degree')
plt.xlabel('Degree')
plt.ylabel('Frequency')
plt.legend()
plt.show()
