class Node: 
    def __init__(self, value):
        self.value = value
        self.next = None
        self.previous = None

    def self_loop(self):
        self.next = self
        self.previous = self

class LinkedCircle:
    @staticmethod
    def scroll_clockwise(node, scroll):
        current_node = node
        while scroll:
            if scroll > 0:
                current_node = current_node.next
                scroll -= 1
            else:
                current_node = current_node.previous
                scroll += 1

        return current_node

    @staticmethod
    def insert_clockwise(node, node_to_add):
        next_node = node.next
        node.next = node_to_add
        next_node.previous = node_to_add

        node_to_add.previous = node
        node_to_add.next = next_node

    @staticmethod
    def remove(node):
        previous_node = node.previous
        next_node = node.next
        
        previous_node.next = next_node
        next_node.previous = previous_node

        return next_node

    @staticmethod
    def print(node):
        visited = set()
        current_node = node
        to_print = []
        while current_node.value not in visited:
            visited.add(current_node.value)
            to_print.append(str(current_node.value))
            current_node = current_node.next

        print(' -> '.join(to_print))




def solve(number_of_players, max_points):
    scores = [0] * (number_of_players + 1)

    current = Node(0)
    zero_node = current
    current.self_loop()
    player = 0

    for marable in range(1, max_points + 1):
        player = (player % number_of_players) + 1

        if marable % 23 == 0:
            scores[player] += marable
            node_to_del = LinkedCircle.scroll_clockwise(current, -7)
            scores[player] += node_to_del.value
            current = LinkedCircle.scroll_clockwise(node_to_del, 1)
            LinkedCircle.remove(node_to_del)
            continue

        place_to_insert = LinkedCircle.scroll_clockwise(current, 1)
        marable_node = Node(marable)
        LinkedCircle.insert_clockwise(place_to_insert, marable_node)
        current = marable_node

    return max(scores)

result = solve(419, 72164 * 100)
print(result)
