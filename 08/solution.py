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


description = get_tree_description()
root = get_tree(description)

to_visit = [root]
sum_of_metadata = 0


while to_visit:
    current_node = to_visit.pop()
    sum_of_metadata += sum(current_node.metadata)

    to_visit += current_node.child_nodes

print(sum_of_metadata)
