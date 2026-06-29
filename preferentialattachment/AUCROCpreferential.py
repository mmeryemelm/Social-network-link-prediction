import networkx as nx
import matplotlib.pyplot as plt
from tabulate import tabulate
import os


def preferential_attachment_score(graph, node1, node2):
    """
    Preferential Attachment Index
    Score = degree(node1) × degree(node2)
    
    Based on idea that nodes with high degree are more likely to connect
    """
    degree1 = graph.degree(node1)
    degree2 = graph.degree(node2)
    return degree1 * degree2


def get_predicted_edges_pa(graph, node, threshold=10):
    """Get predicted edges using Preferential Attachment"""
    predicted = []
    for neighbor in graph.nodes():
        if neighbor != node and not graph.has_edge(node, neighbor):
            score = preferential_attachment_score(graph, node, neighbor)
            if score > threshold:
                predicted.append((node, neighbor, score))
    
    predicted.sort(key=lambda x: x[2], reverse=True)
    return predicted


def load_network_from_mtx(mtx_file):
    """Load graph from Matrix Market format"""
    G = nx.DiGraph()
    
    try:
        with open(mtx_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('%') or not line:
                    continue
                
                try:
                    parts = [int(x) for x in line.split()[:2]]
                    if len(parts) == 2:
                        G.add_edge(parts[0], parts[1])
                except (ValueError, IndexError):
                    continue
        
        print(f"✓ Network loaded: {len(G.nodes())} nodes, {len(G.edges())} edges")
        return G
    
    except FileNotFoundError:
        print(f"✗ File not found: {mtx_file}")
        return None


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mtx_files = [f for f in os.listdir(current_dir) if f.endswith('.mtx')]
    
    if not mtx_files:
        print("✗ Place .mtx file in same directory")
        return
    
    mtx_file = os.path.join(current_dir, mtx_files[0])
    G = load_network_from_mtx(mtx_file)
    
    if G is None:
        return
    
    while True:
        try:
            node = int(input("\nEnter node ID (or -1 to exit): "))
            if node == -1:
                break
            
            if node not in G.nodes():
                print("✗ Node not found")
                continue
            
            predictions = get_predicted_edges_pa(G, node, threshold=1)
            
            if predictions:
                print(f"\nPreferential Attachment Predictions for Node {node}:")
                table = [[i, target, f"{score:.0f}"] for i, (_, target, score) in enumerate(predictions[:10], 1)]
                print(tabulate(table, headers=["Rank", "Node", "Score"], tablefmt="grid"))
            else:
                print("No predictions found")
        
        except ValueError:
            print("✗ Invalid input")


if __name__ == "__main__":
    main()
