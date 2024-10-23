from collections import defaultdict

class CompressedGraph:
    def __init__(self, sccs, original_graph):
        # Constructor to create a compressed graph based on SCCs.
        # The SCCs and the original graph are passed as arguments.
        # `self.graph` will store the compressed version of the graph.
        self.sccs = sccs  # List of strongly connected components (SCCs)
        self.scc_map = self.map_sccs_to_nodes()  # Map each node to its corresponding SCC
        self.graph = defaultdict(set)  # Initialize the compressed graph where edges are sets (to avoid duplicates)

        # Loop through all nodes and edges in the original graph to create the compressed graph
        for u in original_graph.graph:
            for v in original_graph.graph[u]:
                scc_u = self.scc_map[u]  # Find the SCC that contains node u
                scc_v = self.scc_map[v]  # Find the SCC that contains node v
                # Only add an edge between two SCCs if they are different
                if scc_u != scc_v:
                    self.graph[scc_u].add(scc_v)  # Add an edge from SCC of u to SCC of v

    def map_sccs_to_nodes(self):
        """ 
        Maps each node (airport) to the index of the SCC it belongs to.
        This will allow us to compress the graph by grouping nodes in the same SCC together.
        """
        scc_map = {}  # Dictionary to map each node to its SCC index

        # Loop through each SCC and each node in that SCC
        for idx, component in enumerate(self.sccs):
            for airport in component:
                # Assign the SCC index (idx) to each node (airport) in the component
                scc_map[airport] = idx

        return scc_map  # Return the mapping of nodes to SCC indices