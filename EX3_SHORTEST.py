import networkx as nx
import matplotlib.pyplot as plt

# Create a weighted graph
G = nx.Graph()

# Add edges (u, v, weight)
edges = [
    ("A", "B", 4),
    ("A", "C", 2),
    ("B", "C", 1),
    ("B", "D", 5),
    ("C", "D", 8),
    ("C", "E", 10),
    ("D", "E", 2)
]

# Add edges with weights to the graph
G.add_weighted_edges_from(edges)

# Function to print routing table for a node
def print_routing_table(source):
    all_shortest_paths = nx.single_source_dijkstra_path(G, source=source, weight="weight")
    all_shortest_distances = nx.single_source_dijkstra_path_length(G, source=source, weight="weight")

    print(f"\nRouting Table for source node {source}:")
    print("-" * 55)
    print(f"{'Destination':<12}{'Path':<30}{'Cost'}")
    print("-" * 55)
    for dest in all_shortest_paths:
        path = " -> ".join(all_shortest_paths[dest])
        cost = all_shortest_distances[dest]
        print(f"{dest:<12}{path:<30}{cost}")
    print("-" * 55)

    return all_shortest_paths

# Print routing tables for every node
for node in G.nodes():
    print_routing_table(node)

# ---- Visualization (optional) ----
# Show one example routing table visualization (for node A)

source = "A"
all_shortest_paths = nx.single_source_dijkstra_path(G, source=source, weight="weight")

pos = nx.spring_layout(G, seed=42)  # Layout
edge_labels = nx.get_edge_attributes(G, "weight")

plt.figure(figsize=(8,6))
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=1200, font_size=12, font_weight="bold")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Highlight all shortest paths from the chosen source
path_edges = []
for dest, path in all_shortest_paths.items():
    path_edges += list(zip(path, path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color="red")

plt.title(f"Routing Table Visualization for Source Node {source}")
plt.show()
