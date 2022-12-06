import advent
import readchar
import numpy as np
from advent.intcode import run

class IO():

    pieces = {0: 'X', 1: '.', 2: '!', 3: 'o', 4: '?', 5: 's'}

    def __init__(self):
        self.output = 1
        self.maze = {(0, 0): 1}
        self.position = (0, 0)
        self.direction = (0, 0)
    
    def print(self):
        min_x = min(self.maze.keys(), key=lambda a: a[1])[1]
        max_x = max(self.maze.keys(), key=lambda a: a[1])[1]
        min_y = min(self.maze.keys(), key=lambda a: a[0])[0]
        max_y = max(self.maze.keys(), key=lambda a: a[0])[0]
        grid = np.ones((max_y-min_y+1, max_x-min_x+1)) * 4
        for k in self.maze:
            a, b = k
            grid[a-min_y, b-min_x] = self.maze[k]
        grid[self.position[0]-min_y, self.position[1]-min_x] = 3
        grid[0-min_y, 0-min_x] = 5
        output = [''.join(map(lambda x: self.pieces[x], line)) for line in grid]
        print("\033c", end="") # clear terminal
        print('\n'.join(output), flush=True)
    
    def handle_output(self):
        # Position is the 'old' position
        if self.output == 1: # empty spot
            self.position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])
            self.maze[self.position] = 1
        elif self.output == 2:
            self.position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])
            self.maze[self.position] = 2
        elif self.output == 0:
            tmp_position = (self.position[0] + self.direction[0], self.position[1] + self.direction[1])
            self.maze[tmp_position] = 0

    def read(self):
        self.handle_output()
        self.print()
        result = None
        while result not in ['1', '2', '3', '4', 'w', 'a', 's', 'd']:
            result = readchar.readkey()
        if result in ['w', 'a', 's', 'd']: result = {'w': 1, 'a': 3, 's': 2, 'd': 4}[result]
        self.direction = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}[int(result)]
        return int(result)

    def write(self, value):
        self.output = value
        return self

    def output(self):
        return self.maze

data = advent.get_intcode(15)
io = IO()

_, out = run(data.copy(), io)