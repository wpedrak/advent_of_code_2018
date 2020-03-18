from collections import defaultdict, deque

def get_regexp():
    filename = 'input'
    file = open(f"{filename}.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines[0][1:-1]


def build_graph_with_positions(regexp, positions_arg, begin_idx, end_idx):
    positions = set(positions_arg)
    edges = set()
    idx = begin_idx

    while idx < end_idx:
        item = regexp[idx]
        if item in 'NSWE':
            new_edges, shifted_positions = move_positions(positions, item)
            edges = edges | new_edges
            positions = shifted_positions
            idx += 1
            continue
        if item in '(':
            matching_idx = find_matching_bracket(regexp, idx)
            options = get_options(regexp, idx+1, matching_idx)
            new_edges = set()
            new_positions = set()
            for option_from, option_to in options:
                edges_from_option, positions_from_option = build_graph_with_positions(
                    regexp, 
                    positions,
                    option_from,
                    option_to
                )
                new_edges = new_edges | edges_from_option
                new_positions = new_positions | positions_from_option
            edges = edges | new_edges
            positions = new_positions
            idx = matching_idx + 1
            continue

        raise Exception(f'Unexpected item: {item}')

    return edges, positions


def move_positions(positions, item):
    dx, dy = {
        'N': (0, 1),
        'S': (0, -1),
        'W': (-1, 0),
        'E': (1, 0),
    }[item]

    new_positions = set((x+dx, y+dy) for x, y in positions)
    edges = set(zip(positions, new_positions))

    return edges, new_positions


def find_matching_bracket(string, idx):
    idx = idx
    balance = 1

    while balance:
        idx += 1
        item = string[idx]
        balance += item == '('
        balance -= item == ')'

    return idx


def get_options(regexp, begin_idx, end_idx):
    balance = 0
    option_begin_idx = begin_idx
    options = []

    for idx in range(begin_idx, end_idx):
        item = regexp[idx]
        balance += item == '('
        balance -= item == ')'

        if item != '|':
            continue
        if balance:
            continue

        options.append((option_begin_idx, idx))
        option_begin_idx = idx + 1

    options.append((option_begin_idx, end_idx))
    return options


def build_graph(regexp):
    list_edges, _ = build_graph_with_positions(regexp, [(0, 0)], 0, len(regexp))
    edges = defaultdict(lambda: [])

    for v1, v2 in list_edges:
        edges[v1].append(v2)
        edges[v2].append(v1)

    return edges


def find_furtherst(edges, starting_point=(0,0)):
    visited = set()
    to_visit = deque([starting_point, 'DIST++'])
    distance = 0

    while len(to_visit) > 1:
        item = to_visit.popleft()

        if item == 'DIST++':
            distance += 1
            to_visit.append('DIST++')
            continue

        if item in visited:
            continue

        visited.add(item)

        neighbours = edges[item]
        to_visit += [n for n in neighbours if n not in visited]

    return distance


regexp = get_regexp()
print('building graph')
graph = build_graph(regexp)
print('finding furthest')
result = find_furtherst(graph)

print(result)