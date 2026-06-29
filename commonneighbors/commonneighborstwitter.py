import networkx as nx
import matplotlib.pyplot as plt
from tabulate import tabulate
import os
import sys

def common_neighbors_ratio(graph, node1, node2):
    """
    Calculate the ratio of common neighbors between two nodes
    Using Jaccard similarity: |A∩B| / |A∪B|
    """
    out_neighbors1 = set(graph.successors(node1))
    in_neighbors2 = set(graph.predecessors(node2))

    common_neighbors = out_neighbors1.intersection(in_neighbors2)
    union_neighbors = out_neighbors1.union(in_neighbors2)

    if len(union_neighbors) == 0:
        return 0

    ratio = len(common_neighbors) / len(union_neighbors)
    return ratio


def get_predicted_edges(graph, node, threshold=0.2):
    """
    Get predicted future edges for a given node
    Returns edges with score above threshold
    """
    predicted_edges = []
    for neighbor in graph.nodes():
        if neighbor != node and not graph.has_edge(node, neighbor):
            ratio = common_neighbors_ratio(graph, node, neighbor)
            if ratio > threshold:
                predicted_edges.append((node, neighbor, ratio))
    
    # Sort by score (descending)
    predicted_edges.sort(key=lambda x: x[2], reverse=True)
    return predicted_edges


def plot_subgraph(graph, node, predicted_edges, show_plot=True):
    """
    Visualize the subgraph with existing and predicted edges
    Black edges = existing connections
    Red edges = predicted future connections
    """
    try:
        plt.figure(figsize=(12, 8))
        
        # Get all relevant nodes
        all_nodes = [node] + [neighbor for _, neighbor, _ in predicted_edges[:10]]  # Top 10 predictions
        subgraph = graph.subgraph(all_nodes)
        
        # Create layout
        pos = nx.spring_layout(subgraph, k=0.5, iterations=50)
        
        # Get existing edges
        existing_edges = [(u, v) for u, v in graph.edges() if (u in all_nodes and v in all_nodes)]
        predicted_edges_subset = predicted_edges[:10]
        
        # Draw edges
        nx.draw_networkx_edges(subgraph, pos, edgelist=existing_edges, 
                              edge_color='black', width=2.0, alpha=0.6, label='Existing edges')
        nx.draw_networkx_edges(subgraph, pos, edgelist=[(u, v) for u, v, _ in predicted_edges_subset], 
                              edge_color='red', width=2.0, alpha=0.6, style='dashed', label='Predicted edges')
        
        # Draw nodes
        node_colors = ['lightgreen' if n == node else 'lightblue' for n in subgraph.nodes()]
        nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, node_size=400, alpha=0.9)
        nx.draw_networkx_labels(subgraph, pos, font_size=10, font_weight='bold')
        
        plt.title(f'Link Prediction for Node {node}\n(Green=Target, Blue=Neighbors)', fontsize=14, fontweight='bold')
        plt.legend(loc='upper left', fontsize=10)
        plt.axis('off')
        plt.tight_layout()
        
        if show_plot:
            plt.show()
        
        return plt
        
    except Exception as e:
        print(f"Error plotting subgraph: {str(e)}")
        return None


def load_network_from_mtx(mtx_file):
    """
    Load network from Matrix Market (.mtx) format file
    Returns a NetworkX DiGraph (directed graph)
    """
    G = nx.DiGraph()
    
    try:
        with open(mtx_file, 'r') as file:
            # Skip comments and header
            line_count = 0
            for line in file:
                line = line.strip()
                
                # Skip comments (lines starting with %)
                if line.startswith('%'):
                    continue
                
                # Skip first metadata line if not a comment
                if line_count == 0:
                    line_count += 1
                    continue
                
                try:
                    # Parse edge
                    parts = line.split()
                    if len(parts) >= 2:
                        source = int(parts[0])
                        target = int(parts[1])
                        G.add_edge(source, target)
                except ValueError:
                    continue
        
        print(f"✓ Loaded network: {len(G.nodes())} nodes, {len(G.edges())} edges")
        return G
        
    except FileNotFoundError:
        print(f"✗ Error: File not found: {mtx_file}")
        print("  Make sure the .mtx file is in the same directory as this script")
        return None
    except Exception as e:
        print(f"✗ Error loading network: {str(e)}")
        return None


def interactive_prediction():
    """
    Interactive mode to predict links for a specific node
    """
    # Find the .mtx file in current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mtx_files = [f for f in os.listdir(current_dir) if f.endswith('.mtx')]
    
    if not mtx_files:
        print("✗ No .mtx files found in current directory")
        print("  Place your soc-twitter-follows.mtx file here")
        return
    
    mtx_file = os.path.join(current_dir, mtx_files[0])
    print(f"Loading from: {mtx_file}")
    
    # Load network
    G = load_network_from_mtx(mtx_file)
    if G is None:
        return
    
    print(f"\nNetwork Statistics:")
    print(f"  Nodes: {len(G.nodes())}")
    print(f"  Edges: {len(G.edges())}")
    print(f"  Average degree: {sum(dict(G.degree()).values()) / len(G.nodes()):.2f}")
    
    # Interactive loop
    while True:
        try:
            node_input = input("\nEnter node ID to predict links (or 'quit' to exit): ").strip()
            
            if node_input.lower() == 'quit':
                break
            
            node = int(node_input)
            
            if node not in G.nodes():
                print(f"✗ Node {node} not in graph")
                continue
            
            # Get predictions
            predictions = get_predicted_edges(G, node, threshold=0.1)
            
            if not predictions:
                print(f"No predictions found for node {node}")
                continue
            
            # Display results
            print(f"\n{'='*70}")
            print(f"Top 10 Predicted Connections for Node {node}:")
            print(f"{'='*70}")
            
            table_data = []
            for i, (source, target, score) in enumerate(predictions[:10], 1):
                table_data.append([i, target, f"{score:.4f}", f"{score*100:.2f}%"])
            
            headers = ["Rank", "Predicted Node", "Score", "Confidence"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            # Visualize
            show_viz = input("\nVisualize predictions? (y/n): ").lower().strip()
            if show_viz == 'y':
                plot_subgraph(G, node, predictions)
        
        except ValueError:
            print("✗ Invalid input. Please enter a valid node ID")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"✗ Error: {str(e)}")


if __name__ == "__main__":
    interactive_prediction()
