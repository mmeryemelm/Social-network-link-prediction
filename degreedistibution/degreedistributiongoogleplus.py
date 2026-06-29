import networkx as nx
import matplotlib.pyplot as plt

# Chargement du graphe depuis le fichier
G = nx.read_edgelist(r'C:\Users\DELL\Desktop\complexiteprjtfinal\soc-google-plus.txt', create_using=nx.DiGraph(), nodetype=int)

# Fonction pour calculer l'histogramme des degrés
def degree_histogram_directed(G, in_degree=False, out_degree=False):
    nodes = G.nodes()
    if in_degree:
        in_degree = dict(G.in_degree())
        degseq = [in_degree.get(k, 0) for k in nodes]
    elif out_degree:
        out_degree = dict(G.out_degree())
        degseq = [out_degree.get(k, 0) for k in nodes]
    else:
        degseq = [v for k, v in G.degree()]
    dmax = max(degseq) + 1
    freq = [0 for d in range(dmax)]
    for d in degseq:
        freq[d] += 1
    return freq

# Calcul de l'histogramme des degrés pour les degrés entrants et sortants
in_degree_freq = degree_histogram_directed(G, in_degree=True)
out_degree_freq = degree_histogram_directed(G, out_degree=True)

# Print the degree sequences for debugging
print("In-degree sequence:", in_degree_freq)
print("Out-degree sequence:", out_degree_freq)

# Tracé de la distribution des degrés
degrees = range(len(in_degree_freq))
plt.figure(figsize=(12, 8))
plt.loglog(range(len(in_degree_freq)), in_degree_freq, 'go-', label='in-degree')
plt.loglog(range(len(out_degree_freq)), out_degree_freq, 'bo-', label='out-degree')
plt.xlabel('Degree')
plt.ylabel('Frequency')
plt.legend()

plt.show()
