from collections import defaultdict

class OriginalGraph:
    def __init__(self):
        # Initialize the graph as a dictionary where each node has a list of its neighbors
        # defaultdict(list) ensures that if a key (node) is not present, it returns an empty list.
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        # Adds a directed edge from node u to node v
        # If u or v are not already in the graph, add them as empty lists first
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)

    def dfs(self, v, visited, stack):
        # Standard Depth-First Search (DFS) algorithm
        # Marks the current node (v) as visited
        visited[v] = True
        
        # Recursively visit all the neighbors of the current node (v)
        for neighbor in self.graph[v]:
            if not visited[neighbor]:
                self.dfs(neighbor, visited, stack)
        
        # After visiting all neighbors, add the node (v) to the stack
        # The stack is used to maintain the order of finished nodes (for SCC detection)
        stack.append(v)

    def transpose(self):
        # Creates and returns the transpose of the current graph
        # The transpose of a graph is a graph with the same set of vertices, but with all the edges reversed
        g_t = OriginalGraph()  # Create a new graph (transpose)
        
        # For each node u and each of its neighbors v in the original graph,
        # add a reversed edge from v to u in the transpose graph.
        for u in self.graph:
            for v in self.graph[u]:
                g_t.add_edge(v, u)
        
        # Return the transposed graph
        return g_t

    def fill_order(self, visited, stack):
        # This function ensures that all nodes are visited in the order of their "finish time"
        # It performs DFS on each node in the graph to determine this order.
        
        # For every node (airport) in the graph, perform DFS if the node has not been visited
        for airport in self.graph:
            if not visited[airport]:
                self.dfs(airport, visited, stack)

    def dfs_scc(self, v, visited, component):
        # Similar to the DFS function, but instead of filling a stack, this collects all nodes
        # that belong to the same strongly connected component (SCC).
        visited[v] = True
        
        # Add the current node (v) to the current component (SCC)
        component.append(v)
        
        # Visit all neighbors recursively to add them to the same SCC
        for neighbor in self.graph[v]:
            if not visited[neighbor]:
                self.dfs_scc(neighbor, visited, component)

    def find_sccs(self):
        # Main function to find and return all Strongly Connected Components (SCCs) in the graph
        stack = []  # Stack to store nodes by their finish time in DFS order
        visited = {airport: False for airport in self.graph}  # Mark all nodes as not visited

        # Step 1: Fill nodes in the stack according to their finishing times during DFS
        self.fill_order(visited, stack)

        # Step 2: Transpose the graph (reverse the direction of all edges)
        transposed_graph = self.transpose()

        # Step 3: Perform DFS on the transposed graph, using the order in the stack (reverse finishing times)
        visited = {airport: False for airport in self.graph}  # Reset visited for the new DFS
        sccs = []  # List to store all SCCs

        # Process all nodes in the order defined by the stack (last to first)
        while stack:
            v = stack.pop()  # Get the node with the highest finishing time
            if not visited[v]:
                component = []  # To store the current SCC
                # Perform DFS on the transposed graph starting from node v
                transposed_graph.dfs_scc(v, visited, component)
                # Add the found SCC to the list of SCCs
                sccs.append(component)

        # Return the list of SCCs found
        return sccs
