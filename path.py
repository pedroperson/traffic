from random import choice, sample


class Path:
    def __init__(self, map_x, map_y, start=(0, 0), end=(1, 1)):
        self.s = start
        self.e = end
        self.index = 0
        self.path: list[tuple[int, int]] = generate_random_path(
            map_x, map_y, start, end
        )

    # Call this to move to the next target
    def step(self):
        self.index += 1

    def target(self):
        return self.path[self.index]

    def next_target(self):
        if self.index + 1 >= len(self.path):
            return None
        return self.path[self.index + 1]

    def start(self):
        return self.s

    def end(self):
        return self.e


def generate_random_path(map_x, map_y, start=(0, 0), end=(1, 1)):
    def dfs(pos, path):
        x, y = pos
        if not (0 <= x < map_x and 0 <= y < map_y) or pos in path:
            return
        path.append(pos)
        if pos == end:
            paths.append(path.copy())
        else:
            # Only move towards the end point
            moves = []
            if x < end[0]:  # If current x is less than end x, can move down
                moves.append((1, 0))
            if y < end[1]:  # If current y is less than end y, can move right
                moves.append((0, 1))
            if x > end[0]:  # If current x is greater than end x, can move up
                moves.append((-1, 0))
            if y > end[1]:  # If current y is greater than end y, can move left
                moves.append((0, -1))
            for dx, dy in sample(moves, len(moves)):
                dfs((x + dx, y + dy), path)
        path.pop()

    paths = []
    dfs(start, [])
    return choice(paths) if paths else None
