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

def run(code, io, pointer=0, relative=0, steps=-1):
    while pointer >= 0 and steps != 0:
        code, pointer, relative, io = step(code, pointer, relative, io)
        steps -= 1
    return (code, pointer, relative), io.output()