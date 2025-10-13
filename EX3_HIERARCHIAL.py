
import networkx as nx

class HierarchicalRouting:
    def __init__(self):
        self.graph = nx.Graph()
        self.clusters = {}  # node -> cluster mapping
        self.gateways = {}  # cluster -> gateway node

    def add_link(self, u, v, weight=1):
        """Add a bidirectional link"""
        self.graph.add_edge(u, v, weight=weight)

    def assign_cluster(self, node, cluster):
        """Assign a node to a cluster (region)"""
        self.clusters[node] = cluster

    def set_gateway(self, cluster, node):
        """Mark a gateway node for the cluster"""
        self.gateways[cluster] = node

    def find_path(self, src, dest):
        """Hierarchical routing: inside cluster, else via gateways"""
        src_cluster = self.clusters[src]
        dest_cluster = self.clusters[dest]

        if src_cluster == dest_cluster:
            # Intra-cluster → normal shortest path
            return nx.shortest_path(self.graph, src, dest, weight="weight")

        else:
            # Inter-cluster → go via gateways
            src_gateway = self.gateways[src_cluster]
            dest_gateway = self.gateways[dest_cluster]

            path1 = nx.shortest_path(self.graph, src, src_gateway, weight="weight")
            path2 = nx.shortest_path(self.graph, src_gateway, dest_gateway, weight="weight")
            path3 = nx.shortest_path(self.graph, dest_gateway, dest, weight="weight")

            # Combine paths
            return path1[:-1] + path2[:-1] + path3

# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    net = HierarchicalRouting()

    # Build network
    net.add_link("A", "B")
    net.add_link("B", "C")
    net.add_link("C", "D")
    net.add_link("E", "F")
    net.add_link("F", "G")
    net.add_link("C", "E")  # connection between clusters

    # Assign clusters
    for node in ["A", "B", "C", "D"]:
        net.assign_cluster(node, "Cluster1")
    for node in ["E", "F", "G"]:
        net.assign_cluster(node, "Cluster2")

    # Define gateways
    net.set_gateway("Cluster1", "C")
    net.set_gateway("Cluster2", "E")

    # Test routes
    print("Path A → D:", net.find_path("A", "D"))
    print("Path A → G:", net.find_path("A", "G"))