import matplotlib.pyplot as plt
import networkx as nx

def plot_graph(edges,title):
    G = nx.Graph()
    tuple_edges = []
    for edge in edges:
        tuple_edges.append(tuple(edge))
    G.add_edges_from(tuple_edges)
    pos = nx.spring_layout(G)
    plt.title(f"{title}:")
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=16)
    filename = f"{title}.png"       
    plt.savefig(filename)
    plt.close()