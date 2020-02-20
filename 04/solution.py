from datetime import datetime

DATE_BEGIN_POS = 1
DATE_END_POS = 17
ACTION_BEGIN_POS = 19

WAKE_UP = "WAKE_UP"
FALLS_ASLEEP = "FALLS_ASLEEP"
CHANGE = "CHANGE"


def parse_entry(entry):
    date_part = entry[DATE_BEGIN_POS:DATE_END_POS]
    action_part = entry[ACTION_BEGIN_POS:]
    event_datetime = datetime.strptime(date_part, '%Y-%m-%d %H:%M')

    return (event_datetime, action_part)


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


lines = get_lines()
entries = [parse_entry(line) for line in lines]
sorted_entries = sorted(entries, key=lambda x: x[0])

print(sorted_entries)


# print(result)
