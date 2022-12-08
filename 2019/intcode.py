from advent.intcode import run

class IO():
    # Generic interactive asciicode runner
    # accepts input and output, and will append `\n` to every input!

    def __init__(self, input_=[]):
        self.input_buffer = input_.copy()
        self.output_buffer = []
    
    def add_input(self, value):
        for c in value:
            self.input_buffer.append(ord(c))
        return self

    def read(self):
        if len(self.input_buffer) == 0:
            self.handle_output()
            self.add_input(input() + '\n')
        return self.input_buffer.pop(0)
    
    def write(self, value):
        self.output_buffer.append(value)
        return self
    
    def output(self):
        return self.output_buffer
    
    def handle_output(self):
        if CLR:
            print("\033c", end="") # clear terminal
        out = ''.join([chr(v) for v in self.output()[:-1]])
        self.output_buffer = []
        print(out, flush=True)

if __name__ == '__main__':
    import advent
    import sys
    if len(sys.argv) > 2:
        day, part = int(sys.argv[1]), int(sys.argv[2])
    else:
        day, part = 25, 1
    # These are parts that are (interactive?) ascii-compute
    CLR = False

    data = advent.get_intcode(day)
    if day == 17:
        data[0] = part

    io = IO()
    if len(sys.argv) > 3:
        io.add_input(sys.argv[3].replace('\\n', '\n').replace('->', '\n') + '\n')
    run(data.copy(), io)
    if len(io.output()) > 2: # The 2 is kinda random here. it is assumed that anything longer than that
        # is an exit message, anything shorter is a result
        io.handle_output()
    print(io.output()) # leftover need not be ascii
