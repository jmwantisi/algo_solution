def calculate_in_degrees(compressed_graph):
    # Initialize the in-degrees dictionary for each SCC with 0.
    # The dictionary keys are SCCs (0 to number of SCCs - 1), and values are in-degrees.
    in_degrees = {scc: 0 for scc in range(len(compressed_graph.sccs))}

    # Iterate over all the SCCs in the compressed graph (u represents the source SCC).
    for u in compressed_graph.graph:
        # For each SCC u, go through all the SCCs (v) that it has edges to.
        for v in compressed_graph.graph[u]:
            # Increment the in-degree of SCC v because there is an incoming edge from SCC u to SCC v.
            in_degrees[v] += 1

    # Return the dictionary containing the in-degrees of all SCCs.
    return in_degrees


def find_additional_routes(compressed_graph, start_scc):
    # Calculate the in-degrees of all SCCs using the helper function `calculate_in_degrees`.
    in_degrees = calculate_in_degrees(compressed_graph)

    # Initialize a counter for additional routes needed.
    additional_routes_needed = 0

    # Loop through all the SCCs and their in-degrees.
    for scc, in_degree in in_degrees.items():
        # Check if an SCC has no incoming edges (in-degree = 0) and it is not the start SCC.
        if in_degree == 0 and scc != start_scc:
            # If the SCC has no incoming edges and it's not the starting SCC,
            # it means we need at least one new route to make this SCC reachable.
            additional_routes_needed += 1

    # Return the total number of additional routes needed to make all SCCs reachable.
    return additional_routes_needed
