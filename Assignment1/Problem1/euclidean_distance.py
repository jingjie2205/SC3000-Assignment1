import json
import math
from pathlib import Path

base_path = Path(__file__).resolve().parent

coord_path = base_path.parent / "data" / "Coord.json"
heuristic_path = base_path.parent / "data" / "heuristic.json"

# Load coordinates
with open(coord_path, "r") as f:
    coords = json.load(f)

source_node = "50"
x_goal, y_goal = coords[source_node]

# heuristic function from all nodes to source nodes (node #50)
heuristic = {}

for node, (x, y) in coords.items():
    dx = x - x_goal
    dy = y - y_goal
    distance = math.sqrt(dx**2 + dy**2)

    heuristic[node] = distance

# Save
with open(heuristic_path, "w") as f:
    json.dump(heuristic, f, indent=4)