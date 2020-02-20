from datetime import datetime
from collections import defaultdict

DATE_BEGIN_POS = 1
DATE_END_POS = 17
ACTION_BEGIN_POS = 19

WAKE_UP = "wakes up"
FALLS_ASLEEP = "falls asleep"


def is_change(action):
    return action not in [WAKE_UP, FALLS_ASLEEP]


def get_number(change):
    splited = change.split()
    hashed_number = splited[1]
    return hashed_number[1:]


def parse_entry(entry):
    date_part = entry[DATE_BEGIN_POS:DATE_END_POS]
    action_part = entry[ACTION_BEGIN_POS:]
    event_datetime = datetime.strptime(date_part, '%Y-%m-%d %H:%M')

    detail = action_part

    if is_change(action_part):
        detail = get_number(action_part)

    return (event_datetime, detail)


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


lines = get_lines()
entries = [parse_entry(line) for line in lines]
sorted_entries = sorted(entries, key=lambda x: x[0])

sleep_minutes = defaultdict(lambda: [0]*60)

guard_on_shift = None
last_sleep_minute = None

for entry in sorted_entries:
    date_part = entry[0]
    action_part = entry[1]

    if is_change(action_part):
        guard_on_shift = int(action_part)
        continue

    if action_part == FALLS_ASLEEP:
        last_sleep_minute = date_part.minute if date_part.hour == 0 else 0
        continue

    if action_part == WAKE_UP:
        wake_up_minute = date_part.minute if date_part.hour == 0 else 60
        for minute in range(last_sleep_minute, wake_up_minute):
            sleep_minutes[guard_on_shift][minute] += 1

most_sleepy = max(list(sleep_minutes.items()), key=lambda x: max(x[1]))
print(f'id of most sleepy guard {most_sleepy[0]}')

arg_max = None
curr_max = -1

for minute, sleeps in enumerate(most_sleepy[1]):
    if curr_max < sleeps:
        curr_max = sleeps
        arg_max = minute

print(arg_max)

result = most_sleepy[0] * arg_max

print(result)
