import json
import math

# Load coordinates
with open("./data/Coord.json", "r") as f:
    coords = json.load(f)

source_node = "50"
x_goal, y_goal = coords[source_node]

heuristic = {}

for node, (x, y) in coords.items():
    dx = x - x_goal
    dy = y - y_goal
    distance = math.sqrt(dx**2 + dy**2)
    
    heuristic[node] = distance

# Save to new JSON file
with open("heuristic.json", "w") as f:
    json.dump(heuristic, f, indent=4)