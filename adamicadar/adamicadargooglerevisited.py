import networkx as nx
import matplotlib.pyplot as plt
from tabulate import tabulate
import math
import os


def adamic_adar_score(graph, node1, node2):
    """
    Adamic-Adar Index: Sum of inverse log(degree) of common neighbors
    Formula: Σ 1/log(k(z)) for z ∈ N(u) ∩ N(v)
    
    Better than common neighbors because it weights less-connected nodes higher
    """
    out_neighbors1 = set(graph.successors(node1))
    in_neighbors2 = set(graph.predecessors(node2))
    common = out_neighbors1.intersection(in_neighbors2)
    
    if len(common) == 0:
        return 0
    
    score = 0
    for node in common:
        degree = graph.degree(node)
        if degree > 1:
            score += 1.0 / math.log(degree)
    
    return score


def get_predicted_edges_aa(graph, node, threshold=0.5):
    """Get predicted edges using Adamic-Adar algorithm"""
    predicted = []
    for neighbor in graph.nodes():
        if neighbor != node and not graph.has_edge(node, neighbor):
            score = adamic_adar_score(graph, node, neighbor)
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
                if line.startswith('%'):
                    continue
                if not line:
                    continue
                
                try:
                    parts = [int(x) for x in line.split()[:2]]
                    if len(parts) == 2:
                        G.add_edge(parts[0], parts[1])
                except (ValueError, IndexError):
                    continue
        
        print(f"✓ Loaded: {len(G.nodes())} nodes, {len(G.edges())} edges")
        return G
    
    except FileNotFoundError:
        print(f"✗ File not found: {mtx_file}")
        return None
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None


def main():
    # Find .mtx file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mtx_files = [f for f in os.listdir(current_dir) if f.endswith('.mtx')]
    
    if not mtx_files:
        print("✗ No .mtx file found. Place your data file in the same directory.")
        return
    
    mtx_file = os.path.join(current_dir, mtx_files[0])
    
    # Load graph
    G = load_network_from_mtx(mtx_file)
    if G is None:
        return
    
    # Get predictions for a node
    while True:
        try:
            node = int(input("\nEnter node ID (or -1 to exit): "))
            if node == -1:
                break
            
            if node not in G.nodes():
                print(f"✗ Node not found")
                continue
            
            predictions = get_predicted_edges_aa(G, node, threshold=0.1)
            
            if predictions:
                print(f"\nAdamic-Adar Predictions for Node {node}:")
                table = [[i, target, f"{score:.4f}"] for i, (_, target, score) in enumerate(predictions[:10], 1)]
                print(tabulate(table, headers=["Rank", "Node", "Score"], tablefmt="grid"))
            else:
                print("No predictions found")
        
        except ValueError:
            print("✗ Invalid input")
        except Exception as e:
            print(f"✗ Error: {str(e)}")


if __name__ == "__main__":
    main()
