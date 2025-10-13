import networkx as nx
from collections import deque

class FloodingNetwork:
    def __init__(self):
        self.graph = nx.Graph()

    def add_link(self, u, v):
        """Add a bidirectional link"""
        self.graph.add_edge(u, v)

    def flooding(self, source, destination, max_hops=10):
        """Simulate flooding from source to destination"""
        visited_packets = set()
        queue = deque([(source, [source], 0)])  # (current_node, path, hops)
        delivered_paths = []
        transmissions = 0

        while queue:
            node, path, hops = queue.popleft()
            if hops > max_hops:
                continue
            # check if delivered
            if node == destination:
                delivered_paths.append(path)
                continue

            for neighbor in self.graph.neighbors(node):
                if len(path) > 1 and neighbor == path[-2]:
                    continue  # avoid back edge

                packet_id = (neighbor, tuple(path))
                if packet_id in visited_packets:
                    continue  # avoid duplicate

                visited_packets.add(packet_id)
                transmissions += 1
                queue.append((neighbor, path + [neighbor], hops + 1))

        return delivered_paths, transmissions

# Example Usage
if __name__ == "__main__":
    net = FloodingNetwork()
    net.add_link("A", "B")
    net.add_link("A", "C")
    net.add_link("B", "D")
    net.add_link("C", "D")
    net.add_link("C", "E")
    net.add_link("D", "E")

    source, destination = "A", "E"
    paths, transmissions = net.flooding(source, destination)

    print(f"\nFlooding from {source} to {destination}")
    print(f"Possible delivery paths: {paths}")
    print(f"Total transmissions: {transmissions}")
