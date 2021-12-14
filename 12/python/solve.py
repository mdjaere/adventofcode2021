import sys
from collections import defaultdict
import re

infile = sys.argv[1] if len(sys.argv) > 1 else 'input'
routes = [line.strip().split("-") for line in open(infile)]

tunnels_to = defaultdict(set)
for route in routes:
    a, b = route
    tunnels_to[a].add(b)
    tunnels_to[b].add(a)


def find_connections(route, allow_double=True):
    if route[-1] == "end":
        return [route]
    connections = tunnels_to[route[-1]]
    routes = []
    for dest in connections:
        if dest == "start":
            continue
        if re.search(r'[a-z]', dest):
            if dest in route:
                if allow_double:
                    routes.extend(find_connections(
                        [*route, dest], allow_double=False))
            else:
                routes.extend(find_connections([*route, dest], allow_double))
        else:
            routes.extend(find_connections([*route, dest], allow_double))
    return [route for route in routes if len(route) > 0]


found = find_connections(["start"], allow_double=False)
print(len(found))

found = find_connections(["start"], allow_double=True)
print(len(found))
