import advent
import numpy as np
import readchar
import time
from advent.intcode import run

pieces = {0: ' ', 1: '|', 2: 'X', 3: '-', 4: 'o'}

automatic = 0.03

class IO():
    # Simple implementation of IO: just has static input in the __init__

    def __init__(self, input_=None):
        self.input_buffer = input_ if input_ is not None else []
        self.output_buffer = []
        self.grid = np.ones((20, 44)) # hard coded yeah!
        self.score = 0
    
    def print(self):
        output = [''.join(map(lambda x: pieces[x], line)) for line in self.grid] + [f"Score: {self.score}"]
        print("\033c", end="") # clear terminal
        print('\n'.join(output), flush=True)
    
    def handle_output(self):
        for i in range(0, len(self.output_buffer), 3):
            if self.output_buffer[i] == -1 or self.output_buffer[i+1] == -1:
                self.score = self.output_buffer[i+2]
            else:
                self.grid[self.output_buffer[i+1],self.output_buffer[i]] = self.output_buffer[i+2]
        self.output_buffer = []
        return self

    def read(self):
        if len(self.input_buffer) > 0:
            return self.input_buffer.pop(0)
        self.handle_output()
        self.print()
        if automatic > 0:
            paddle = np.where(self.grid == 3)[1][0]
            ball = np.where(self.grid == 4)[1][0]
            time.sleep(automatic)
            return int(ball > paddle) - int(ball < paddle)
        result = None
        while result not in ['-1', '0', '1', 'a', 's', 'd']:
            result = readchar.readkey()
        if result in ['a', 's', 'd']: result = {'a': -1, 's': 0, 'd': 1}[result]
        return int(result)
    
    def write(self, value):
        self.output_buffer.append(value)
        return self
    
    def output(self):
        return self.output_buffer

code = advent.get_intcode(13)
code[0] = 2 # insert coin
_, out = run(code, IO([]))