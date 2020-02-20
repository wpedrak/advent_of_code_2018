from re import search
from collections import defaultdict


class Worker:
    EMPTY_TASK = '.'

    def __init__(self, factory):
        self.factory = factory
        self.time_working = 0
        self.target = 1
        self.works_on = Worker.EMPTY_TASK
        self.task_finished = False

    def tick(self):
        self.time_working += 1
        if self.time_working == self.target:
            self.finish_task()

    def finish_task(self):
        self.task_finished = True
        if self.works_on == Worker.EMPTY_TASK:
            return

        factory.finish_task(self.works_on)

    def pick_new_task(self):
        if not self.task_finished:
            return

        self.task_finished = False
        self.time_working = 0
        task = factory.get_new_task()
        self.works_on = task

        if task == Worker.EMPTY_TASK:
            self.target = 1
            return

        self.target = ord(task) - ord('A') + 1 + 60


class Factory:
    def __init__(self, to_process, in_deg, edges):
        self.workers = []
        self.to_process = to_process
        self.request_size = len(vertices)
        self.processed = []

        self.in_deg = in_deg
        self.edges = edges

        self.time = -1

    def add_worker(self):
        worker = Worker(self)
        self.workers.append(worker)

    def is_working(self):
        return len(self.processed) != self.request_size

    def tick(self, verbose=False):
        self.time += 1
        if verbose:
            print(self.time, end='')

        for worker in self.workers:
            worker.tick()

        for worker in self.workers:
            worker.pick_new_task()

        if verbose:
            for worker in self.workers:
                print(f'    {worker.works_on}', end='')

            print(f'     {"".join(self.processed)}')

    def get_time(self):
        return self.time

    def get_new_task(self):
        all_possible = list(filter(
            lambda x: in_deg[x] == 0,
            self.to_process
        ))
        if not all_possible:
            return Worker.EMPTY_TASK

        next_task = min(all_possible)
        self.to_process.remove(next_task)

        return next_task

    def finish_task(self, task):
        self.processed.append(task)
        for neighbour in edges[task]:
            in_deg[neighbour] -= 1


def parse_instruction(instruction):
    search_result = search(
        r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.',
        instruction
    )

    return [search_result.group(i) for i in range(1, 3)]


def get_lines():
    file = open("input.txt", "r")
    lines = [line.rstrip('\n') for line in file]
    return lines


lines = get_lines()
edges = defaultdict(lambda: [])
in_deg = defaultdict(lambda: 0)
vertices = set()

for line in lines:
    v_from, v_to = parse_instruction(line)
    vertices.add(v_from)
    vertices.add(v_to)
    edges[v_from].append(v_to)
    in_deg[v_to] += 1

factory = Factory(vertices, in_deg, edges)

for _ in range(5):
    factory.add_worker()

while factory.is_working():
    factory.tick()

print(factory.get_time())
