import json
import heapq
import math

# -----------------------------
# Load data
# -----------------------------
with open("SC3000_AI\\data\\G.json", "r") as f:
    G = json.load(f)        # adjacency list

with open("SC3000_AI\\data\\Coord.json", "r") as f:
    Coord = json.load(f)    # node coordinates

with open("SC3000_AI\\data\\Dist.json", "r") as f:
    Dist = json.load(f)     # distance per edge

with open("SC3000_AI\\data\\Cost.json", "r") as f:
    Cost = json.load(f)     # energy cost per edge

# -----------------------------
# Normalize a dictionary to [0,1]
# -----------------------------
def normalize_dict(d):
    values = list(d.values())
    min_v, max_v = min(values), max(values)
    if max_v - min_v == 0:
        return {k: 0 for k in d}  # avoid division by zero
    return {k: (v - min_v)/(max_v - min_v) for k, v in d.items()}

normalized_dist = normalize_dict(Dist)

# -----------------------------
# Precompute Euclidean heuristic
# -----------------------------
goal_node = "50"
x_goal, y_goal = Coord[goal_node]

heuristic = {}
for node, (x, y) in Coord.items():
    dx = x - x_goal
    dy = y - y_goal
    heuristic[node] = math.sqrt(dx**2 + dy**2)

normalized_heuristic = normalize_dict(heuristic)

# -----------------------------
# A* search with weighted f(n)
# -----------------------------
def a_star(G, Cost, normalized_dist, normalized_heuristic, start, goal, max_energy, alpha=1, beta=1):
    """
    Weighted A* search:
        f(n) = alpha*normalized_dist + beta*normalized_heuristic
        energy cost tracked separately to respect max_energy
    """
    pq = [(0, start, [start], 0)]  # (f(n), node, path, energy_used)
    visited = dict()  # track lowest energy used per node
    nodes_expanded = 0

    while pq:
        f_n, node, path, energy_used = heapq.heappop(pq)
        nodes_expanded += 1

        # Skip if energy exceeded
        if energy_used > max_energy:
            continue

        # Goal check
        if node == goal:
            return path, energy_used, nodes_expanded

        # Skip if already visited with lower energy
        if node in visited and visited[node] <= energy_used:
            continue
        visited[node] = energy_used

        # Explore neighbors
        for neighbor in G.get(node, []):
            edge_key = f"{node},{neighbor}"
            edge_cost = Cost.get(edge_key, float('inf'))
            dist = normalized_dist.get(edge_key, 0)
            h = normalized_heuristic.get(neighbor, 0)

            new_energy = energy_used + edge_cost
            f_new = alpha * dist + beta * h  # weighted priority

            heapq.heappush(pq, (f_new, neighbor, path + [neighbor], new_energy))

    return None, None, nodes_expanded

# -----------------------------
# Run search
# -----------------------------
start_node = "1"
max_energy = 287932
alpha = 1    # weight for edge distance
beta = 2     # weight for heuristic (Euclidean)

path, energy_used, nodes_expanded = a_star(
    G, Cost, normalized_dist, normalized_heuristic, start_node, goal_node, max_energy, alpha, beta
)

if path:
    print(f"Path: {path}")
    print(f"Energy used: {energy_used}")
    print(f"Nodes expanded: {nodes_expanded}")
    print(f"Number of nodes in path: {len(path)}")
else:
    print("No path found within energy limit")