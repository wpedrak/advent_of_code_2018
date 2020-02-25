class Node:
    def __init__(self, child_nodes, metadata):
        self.child_nodes = child_nodes
        self.metadata = metadata

    def __str__(self):
        metadata_str = ','.join([str(x) for x in self.metadata])
        children_nodes_str = ','.join(str(n) for n in self.child_nodes)
        return f'({metadata_str} - {children_nodes_str})'

    def __repr__(self):
        return str(self)


def get_tree_description():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    line = lines[0]

    return [int(x) for x in line.split()]


def get_node(numbers, pos):
    quantity_of_child_nodes = numbers[pos]
    quantity_of_metadata = numbers[pos + 1]

    child_nodes = []
    next_node_idx = pos + 2

    for i in range(quantity_of_child_nodes):
        child_node, end_idx = get_node(numbers, next_node_idx)
        next_node_idx = end_idx
        child_nodes.append(child_node)

    metadata_idx = next_node_idx
    idx_after_node = metadata_idx + quantity_of_metadata

    metadata = numbers[metadata_idx: idx_after_node]

    this_node = Node(child_nodes, metadata)

    return this_node, idx_after_node


def get_tree(numbers):
    node, _ = get_node(numbers, 0)
    return node


def get_node_value(node):
    child_nodes = node.child_nodes
    metadata = node.metadata
    if not child_nodes:
        return sum(metadata)

    node_value = 0

    for idx in metadata:
        if idx < 1 or idx > len(child_nodes):
            continue

        node_value += get_node_value(child_nodes[idx - 1])

    return node_value


description = get_tree_description()
root = get_tree(description)

root_value = get_node_value(root)

print(root_value)
