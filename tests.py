import unittest
from original_graph import OriginalGraph  # Import the class that manages the original graph
from compressed_graph import CompressedGraph  # Import the class that manages the compressed graph
from utils import find_additional_routes  # Import the utility function to calculate additional routes needed

class Tests(unittest.TestCase):
    def setUp(self):
        """
            This method sets up the test environment by initializing the graph and adding edges to it.
            The graph is created using the OriginalGraph class, and a predefined list of edges representing
            flight routes is added to the graph.
        """
        self.graph = OriginalGraph()  # Create an empty graph object

        # List of edges (flight routes) in the graph, each representing a directed connection from one airport to another
        edges = [
            ('DSM', 'ORD'), ('ORD', 'BGI'), ('BGI', 'LGA'), ('LGA', 'JFK'),
            ('JFK', 'HND'), ('HND', 'ICN'), ('ICN', 'HND'), ('SFO', 'SAN'),
            ('SAN', 'EYW'), ('EYW', 'LHR'), ('LHR', 'SFO'), ('TLV', 'DEL'),
            ('DEL', 'DOH'), ('DEL', 'CDG'), ('CDG', 'BUD'), ('CDG', 'SIN'),
            ('SIN', 'CDG')
        ]

        # Add each edge to the graph
        for u, v in edges:
            self.graph.add_edge(u, v)

    def test_sccs(self):
        """
            Test method to find and print all Strongly Connected Components (SCCs) in the graph.
            The SCCs are calculated using the find_sccs() method of the OriginalGraph class.
            The test asserts that there is at least one component with more than one node (strong connectivity).
        """
        sccs = self.graph.find_sccs()  # Find all SCCs in the graph
        print(f"Strongly Connected Components: {sccs}")  # Print the found SCCs

        # Assert that there is at least one component with more than one node (meaning there's strong connectivity)
        self.assertTrue(any(len(component) > 1 for component in sccs))

    def test_compressed_graph(self):
        """
            Test method to compress the graph based on its SCCs and print the compressed graph.
            The graph is compressed using the CompressedGraph class, and the SCCs and connections between them
            are printed to verify the compression.
        """
        sccs = self.graph.find_sccs()  # Find all SCCs in the graph
        compressed_graph = CompressedGraph(sccs, self.graph)  # Compress the graph based on SCCs

        # Print the original graph's adjacency list
        print("\nOriginal Graph:")
        for key, values in self.graph.graph.items():
            print(f"{key} -> {values}")

        # Print the compressed graph's SCCs
        print("\nCompressed Graph (SCC Components):")
        for i, scc in enumerate(compressed_graph.sccs):
            print(f"Component {i}: {scc}")
        
        # Print the edges in the compressed graph (connections between SCCs)
        print("\nCompressed Graph Edges (between SCCs):")
        for u, neighbors in compressed_graph.graph.items():
            for v in neighbors:
                print(f"Strongly Connected Component {u} -> Strongly Connected Component {v}")

        # Assert that the number of SCCs in the compressed graph is smaller than the number of nodes in the original graph
        self.assertTrue(len(compressed_graph.sccs) < len(self.graph.graph))

    def test_additional_routes_needed(self):
        """
            Test method to calculate the minimum number of additional routes needed to make all SCCs reachable
            from different start airports. This is done for each airport in the original graph.
        """
        sccs = self.graph.find_sccs()  # Find all SCCs in the graph
        compressed_graph = CompressedGraph(sccs, self.graph)  # Compress the graph based on SCCs
        
        # Loop through each start airport and calculate the number of additional routes needed
        for start_airport in self.graph.graph.keys():
            # Map the start airport to its corresponding SCC in the compressed graph
            start_scc = compressed_graph.scc_map[start_airport]
            # Calculate the number of additional routes needed to make all SCCs reachable from this start SCC
            routes = find_additional_routes(compressed_graph, start_scc)
            print(f"\nFor start airport {start_airport}, minimum number of routes to be added: {routes}")
            
            # Assert that the number of additional routes needed is non-negative
            self.assertGreaterEqual(routes, 0)

# This block runs the tests when the script is executed directly
if __name__ == "__main__":
    unittest.main()