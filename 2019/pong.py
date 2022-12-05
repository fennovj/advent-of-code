import advent
import numpy as np

pieces = {0: ' ', 1: '|', 2: 'X', 3: '-', 4: 'o'}

class IO():
    # Simple implementation of IO: just has static input in the __init__

    def __init__(self, input_=None):
        self.input_buffer = input_ if input_ is not None else []
        self.output_buffer = []
        self.grid = np.ones((20, 44)) # hard coded yeah!
        self.score = 0
    
    def print(self):
        output = [''.join(map(lambda x: pieces[x], line)) for line in self.grid] + [f"Score: {self.score}"]
        for line in output:
            print(line)
    
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
        result = None
        while result not in ['-1', '0', '1', 'a', 's', 'd']:
            result = input("Your input? (-1=left, 0=stay, 1=right)")
        if result in ['a', 's', 'd']: result = {'a': -1, 's': 0, 'd': 1}[result]
        return int(result)
    
    def write(self, value):
        self.output_buffer.append(value)
        return self
    
    def output(self):
        return self.output_buffer

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

code = advent.get_intcode(13)
code[0] = 2 # insert coin
_, out = run(code, IO([]))