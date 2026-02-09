import networkx as nx
import matplotlib.pyplot as plt

# -----------------------------
# Step 1: Create the Graph
# -----------------------------
G = nx.Graph()

edges = [
    ('A', 'B', 2),
    ('B', 'C', 5),
    ('C', 'D', 4),
    ('D', 'E', 3)
]

G.add_weighted_edges_from(edges)

# -----------------------------
# Step 2: Spanning Tree
# (any spanning tree)
# -----------------------------
spanning_tree = nx.minimum_spanning_tree(G)  # works as spanning tree too

# -----------------------------
# Step 3: Minimum Spanning Tree
# -----------------------------
mst = nx.minimum_spanning_tree(G, algorithm='kruskal')

print("Edges in Minimum Spanning Tree:")
for u, v, w in mst.edges(data=True):
    print(f"{u} - {v} : {w['weight']}")

# -----------------------------
# Step 4: Divisive Clustering
# (remove the largest edges from MST)
# -----------------------------
def divisive_clustering(mst, k):
    """
    mst: Minimum Spanning Tree
    k: number of clusters
    """
    mst_copy = mst.copy()

    # Sort edges by descending weight
    edges_sorted = sorted(
        mst_copy.edges(data=True),
        key=lambda x: x[2]['weight'],
        reverse=True
    )

    # Remove (k-1) largest edges
    for i in range(k - 1):
        u, v, w = edges_sorted[i]
        mst_copy.remove_edge(u, v)

    return list(nx.connected_components(mst_copy))

# Example: divide into 2 clusters
clusters = divisive_clustering(mst, k=2)

print("\nDivisive Clustering Result:")
for i, cluster in enumerate(clusters, 1):
    print(f"Cluster {i}: {cluster}")

# -----------------------------
# Step 5: Visualization
# -----------------------------
pos = nx.spring_layout(G)

plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
nx.draw(G, pos, with_labels=True, node_color='lightblue')
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
plt.title("Original Graph")

plt.subplot(1, 3, 2)
nx.draw(spanning_tree, pos, with_labels=True, node_color='lightgreen')
plt.title("Spanning Tree")

plt.subplot(1, 3, 3)
nx.draw(mst, pos, with_labels=True, node_color='lightcoral')
plt.title("Minimum Spanning Tree")

plt.show()
