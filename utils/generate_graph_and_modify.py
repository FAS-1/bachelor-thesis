import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import sys


def save_graph(G, filename, title, original_edges, special_edges):
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
    nx.draw_networkx_labels(G, pos, font_weight='bold')

    nx.draw_networkx_edges(G, pos, edgelist=original_edges, width=2)
    if special_edges:
        nx.draw_networkx_edges(G, pos, edgelist=special_edges, edge_color='r', style='dashed', width=2)

    plt.title(title)
    plt.axis('off')
    plt.savefig(filename)
    plt.close()


def parse_demands(csv_file):
    df = pd.read_csv(csv_file)
    return [(int(row['Source'][1:]), int(row['Destination'][1:]), row['Data Size (MB)']) for index, row in df.iterrows()]


def can_add_edge(G, node, reconfigurable_edges):
    return len([edge for edge in reconfigurable_edges if node in edge]) < 1


def demand_first(G, demands, reconfigurable_edges):
    demands.sort(key=lambda x: x[2], reverse=True)
    for source, target, _ in demands:
        if not G.has_edge(source, target) and can_add_edge(G, source, reconfigurable_edges) and can_add_edge(G, target,
                                                                                                             reconfigurable_edges):
            G.add_edge(source, target)
            reconfigurable_edges.add((source, target))
    return reconfigurable_edges


def longest_path_first(G, reconfigurable_edges):
    while True:
        try:
            all_shortest_paths = dict(nx.all_pairs_shortest_path_length(G))
            path_list = [(source, target, length) for source, paths in all_shortest_paths.items() for target, length in paths.items() if source != target and can_add_edge(G, source, reconfigurable_edges) and can_add_edge(G, target, reconfigurable_edges)]
            if not path_list:
                break

            source, target, _ = max(path_list, key=lambda x: x[2])
            G.add_edge(source, target)
            reconfigurable_edges.add((source, target))
        except ValueError:
            break
    return reconfigurable_edges


def main(degree, num_nodes, demand_file_path):
    G_initial = nx.random_regular_graph(degree, num_nodes)
    original_edges = list(G_initial.edges())


    save_graph(G_initial, "initial_graph.png", "", original_edges, None)
    edges_list = list(G_initial.edges())
    print("Initial Graph Edges: ", edges_list)

    reconfigurable_edges = set()
    for edge in longest_path_first(G_initial.copy(), reconfigurable_edges):
        pass
    save_graph(G_initial, "longest_path_first_graph.png", "", original_edges,
               reconfigurable_edges)
    print("Longest_Path_First Edges: ", reconfigurable_edges)

    reconfigurable_edges.clear()
    for edge in demand_first(G_initial.copy(), parse_demands(demand_file_path), reconfigurable_edges):
        pass
    save_graph(G_initial, "demand_first_graph.png", "", original_edges, reconfigurable_edges)
    print("Demand_First Edges: ", reconfigurable_edges)

    print("Graphs saved: initial, longest path first, and demand first.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: script.py <degree> <number of nodes> <path_to_transfers_csv>")
        sys.exit(1)

    try:
        degree = int(sys.argv[1])
        num_nodes = int(sys.argv[2])
        demand_file_path = sys.argv[3]
    except ValueError:
        print("Error: Ensure the degree and number of nodes are integers and the path to the CSV file is correct.")
        sys.exit(1)

    if degree < 2 or num_nodes < degree:
        print("Error: Degree must be at least 2 and less than the number of nodes.")
        sys.exit(1)

    main(degree, num_nodes, demand_file_path)
