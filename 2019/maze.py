import advent
import readchar
import numpy as np

def put(code, op, pointer, relative, offset, value):
    mode = op % (10**(2+offset)) // (10**(1+offset))
    if mode == 0: # parameter mode
        ix = code[pointer+offset]
    elif mode == 2: # relative mode
        ix = code[pointer+offset] + relative
    else: raise ValueError(f"{op}, {pointer}, {offset} not allowed")

    if ix >= len(code): # Make sure we allocate enough memory
        code += [0] * (ix - len(code) + 1)
    code[ix] = value

def get(op, code, pointer, relative, offset):
    # e.g. get(1002, code, 2) -> code[p] (immediate mode)
    # e.g. get(2, code, 2) -> code[code[p]] (parameter mode)
    mode = op % (10**(2+offset)) // (10**(1+offset))
    if mode == 0: # parameter mode
        if pointer+offset >= len(code): return 0 if code[0] >= len(code) else code[0]
        if code[pointer+offset] >= len(code): return 0
        return code[code[pointer+offset]]
    elif mode == 1: # immediate mode
        if pointer+offset >= len(code): return 0
        return code[pointer+offset]
    elif mode == 2: # relative mode
        if pointer+offset >= len(code): return 0 if relative+code[0] >= len(code) else code[relative]
        if relative+code[pointer+offset] >= len(code): return 0
        return code[relative+code[pointer+offset]]
    raise ValueError(f"{op}, {pointer}, {offset} not allowed")

def step(code, p, r, io):
    # INPLACE does a intcode step, and returns new state and new p
    op = code[p]
    if op % 100 == 1: # add
        put(code, op, p, r, 3, get(op, code, p, r, 1) + get(op, code, p, r, 2))
        return code, p+4, r, io
    elif op % 100 == 2: # mul
        put(code, op, p, r, 3, get(op, code, p, r, 1) * get(op, code, p, r, 2))
        return code, p+4, r, io
    elif op % 100 == 3: # read
        put(code, op, p, r, 1, io.read())
        return code, p+2, r, io
    elif op % 100 == 4: # write
        return code, p+2, r, io.write(get(op, code, p, r, 1))
    elif op % 100 == 5: # jmp_f
        if get(op, code, p, r, 1) != 0:
            return code, get(op, code, p, r, 2), r, io
        return code, p+3, r, io
    elif op % 100 == 6: # jmp_t
        if get(op, code, p, r, 1) == 0:
            return code, get(op, code, p, r, 2), r, io
        return code, p+3, r, io
    elif op % 100 == 7: # lt
        put(code, op, p, r, 3, int(get(op, code, p, r, 1) < get(op, code, p, r, 2)))
        return code, p+4, r, io
    elif op % 100 == 8: # eq
        put(code, op, p, r, 3, int(get(op, code, p, r, 1) == get(op, code, p, r, 2)))
        return code, p+4, r, io
    elif op % 100 == 9: # relative
        return code, p+2, r + get(op, code, p, r, 1), io
    elif op % 100 == 99: # exit
        return code, -1, r, io
    raise ValueError(f"Incorrect program. Op is {op}")

def run(code, io):
    pointer = 0
    relative = 0
    while pointer >= 0:
        code, pointer, relative, io = step(code, pointer, relative, io)
    return code, io.output()

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