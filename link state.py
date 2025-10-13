import networkx as nx

class LinkStateRouting:
    def __init__(self):
        self.graph = nx.Graph()

    def add_link(self, u, v, weight=1):
        """Add a bidirectional link"""
        self.graph.add_edge(u, v, weight=weight)

    def compute_routing_tables(self):
        """Compute routing table for every node using Dijkstra"""
        routing_tables = {}
        for node in self.graph.nodes():
            lengths, paths = nx.single_source_dijkstra(self.graph, node, weight="weight")
            table = {}
            for dest, path in paths.items():
                if node == dest:
                    table[dest] = ("-", 0, [node])   # self route
                else:
                    next_hop = path[1]  # second node in path
                    table[dest] = (next_hop, lengths[dest], path)
            routing_tables[node] = table
        return routing_tables

# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    net = LinkStateRouting()
    net.add_link("A", "B", 4)
    net.add_link("A", "C", 2)
    net.add_link("B", "C", 1)
    net.add_link("B", "D", 5)
    net.add_link("C", "D", 8)
    net.add_link("C", "E", 10)
    net.add_link("D", "E", 2)

    routing_tables = net.compute_routing_tables()

    # Print results
    for node, table in routing_tables.items():
        print(f"\nRouting table for Node {node}:")
        print(f"{'Dest':<6}{'NextHop':<8}{'Cost':<6}{'Path'}")
        for dest, (nh, cost, path) in table.items():
            print(f"{dest:<6}{nh:<8}{cost:<6}{path}")
