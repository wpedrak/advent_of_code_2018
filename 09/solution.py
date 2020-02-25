

def solve(number_of_players, max_points, verbose=False):
    scores = [0] * (number_of_players + 1)

    circle = [0]
    idx_of_current = 0
    player = 0

    for marable in range(1, max_points + 1):
        player = (player % number_of_players) + 1
        circle_size = len(circle)

        if marable % 23 == 0:
            scores[player] += marable
            del_idx = (idx_of_current - 7) % circle_size
            del_idx = del_idx if del_idx > 0 else del_idx + circle_size
            scores[player] += circle[del_idx]
            del circle[del_idx]
            idx_of_current = del_idx

            if verbose:
                print(f'[{player}] ', end='')
                print(f'({circle[idx_of_current]}) ', end='')
                print(circle)
            continue

        insert_idx = (idx_of_current + 2) % circle_size
        circle.insert(insert_idx, marable)
        idx_of_current = insert_idx

        if verbose:
            print(f'[{player}] ', end='')
            print(f'({circle[idx_of_current]}) ', end='')
            print(circle)

    return max(scores)

result = solve(10, 1618)
# print('')
# print(result)
print(result == 8317)
result = solve(13, 7999)
# print('')
# print(result)
print(result == 146373)
result = solve(17, 1104)
# print('')
# print(result)
print(result == 2764)
result = solve(21, 6111)
# print('')
# print(result)
print(result == 54718)
result = solve(30, 5807)
# print('')
# print(result)
print(result == 37305)

result = solve(419, 72164)
print(result)
