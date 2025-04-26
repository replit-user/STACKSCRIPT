from sys import argv, exit
from collections import defaultdict
import os
import random

functions = defaultdict(list)
program_counter = 0
compare_slot = False
PATH = argv[1]
SIZE = 30000

with open(PATH, "r") as f:
    CODE = f.read().splitlines()

main_code = []

class stack:
    def __init__(self, size):
        self.mem = [0 for _ in range(size)]
        self.pointer = 1

    def push(self, num):
        num = int(num)
        self.mem[self.pointer] = num
        self.pointer += 1

    def pop(self):
        self.pointer -= 1
        return self.mem[self.pointer]

    def top(self):
        return self.mem[self.pointer - 1]

class secondarstack:
    def __init__(self, size):
        self.mem = [0 for _ in range(size)]
        self.pointer = 1

    def push(self, num):
        num = int(num)
        self.mem[self.pointer] = num
        self.pointer += 1

    def top(self):
        return self.mem[self.pointer - 1]

mem = stack(SIZE)
mem2 = secondarstack(SIZE)
jump_occurred = False

def readfunc():
    global main_code, functions
    in_func = False
    current_func = []
    func_name = ""
    main_code = []
    for line in CODE:
        stripped = line.strip()
        if in_func:
            if stripped == "ENDFUNC":
                in_func = False
                functions[func_name] = current_func
                current_func = []
            else:
                if ':' in line:
                    if current_func:
                        functions[func_name] = current_func
                        current_func = []
                    func_name = line.split(':')[0].strip()
                else:
                    current_func.append(line)
        else:
            if ':' in line:
                in_func = True
                func_name = line.split(':')[0].strip()
                current_func = []
            elif stripped == "ENDFUNC":
                continue
            else:
                main_code.append(line)
    if in_func and current_func:
        functions[func_name] = current_func

def execute(instruction: str) -> None:
    global mem, mem2, jump_occurred, program_counter
    jump_occurred = False
    parts = instruction.split(" ")
    parts = [p.strip() for p in parts]
    if not parts:
        return
    opcode = parts[0]
    if ";" in instruction:
        execute(instruction.split(";")[0].strip())
        return
    if opcode == "READ":
        num = input("Enter a number: ").strip()
        try:
            if '.' in num:
                mem.push(float(num))
            else:
                mem.push(int(num))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            exit()
    elif opcode == "SPREAD":
        num = input("Enter a number: ").strip()
        try:
            if '.' in num:
                mem2.push(float(num))
            else:
                mem2.push(int(num))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            exit()
    elif opcode.startswith("JMP"):
        target = int(parts[1]) - 1
        condition_met = False
        if opcode == "JMP":
            condition_met = True
        elif opcode == "JMPGT":
            if mem.top() > int(parts[1]):
                condition_met = True
                target = int(parts[2]) - 1
        elif opcode == "JMPLT":
            if mem.top() < int(parts[1]):
                condition_met = True
                target = int(parts[2]) - 1
        elif opcode == "JMPEQ":
            if mem.top() == int(parts[1]):
                condition_met = True
                target = int(parts[2]) - 1
        if condition_met:
            program_counter = target
            jump_occurred = True
    elif opcode == "PUSH":
        mem.push(parts[1])
    elif opcode == "POP":
        mem.pop()
    elif opcode == "HALT":
        exit()
    elif opcode in {"ADD", "SUB", "MUL", "DIV", "EXP"}:
        b = mem.pop()
        a = mem.pop()
        if opcode == "ADD":
            mem.push(a + b)
        elif opcode == "SUB":
            mem.push(a - b)
        elif opcode == "MUL":
            mem.push(a * b)
        elif opcode == "DIV":
            if b == 0:
                mem.push(0)
            else:
                mem.push(a // b)
        elif opcode == "EXP":
            mem.push(a ** b)
    elif opcode == "OUT":
        print(" ".join(parts[1:]))
    elif opcode == "BOTOP":
        mem.push(mem.mem[0])
    elif opcode == "CLEAR":
        mem = stack(SIZE)
    elif opcode == "CALL":
        func_name = parts[1]
        for instr in functions[func_name]:
            execute(instr)
    elif opcode == "COPY":
        addr = int(parts[1])
        mem.push(mem.mem[addr])
    elif opcode == "DUP":
        mem.push(mem2.top())
    elif opcode == "SPUSH":
        mem2.push(parts[1])
    elif opcode == "PUD":
        mem2.push(mem.top())
    elif opcode == "SWAP":
        addr1 = int(parts[1])
        addr2 = int(parts[2])
        mem.mem[addr1], mem.mem[addr2] = mem.mem[addr2], mem.mem[addr1]
    elif opcode == "SPOUTV":
        print(mem2.top())
    elif opcode == "S-SWAP":
        addr1 = int(parts[1])
        addr2 = int(parts[2])
        mem2.mem[addr1], mem2.mem[addr2] = mem2.mem[addr2], mem2.mem[addr1]
    elif opcode == "READFILE":
        with open(parts[1], "r") as f:
            print(f.read())
    elif opcode == "WRITEFILE":
        with open(parts[1], "w") as f:
            f.write(" ".join(parts[2:]))
    elif opcode == "APPENDFILE":
        with open(parts[1], "a") as f:
            f.write(" ".join(parts[2:]))
    elif opcode == "DELETEFILE":
        os.remove(parts[1])
    elif opcode == "CREATEFILE":
        with open(parts[1], "w") as f:
            f.write(" ".join(parts[2:]))
    elif opcode == "CREATEFOLDER":
        os.mkdir(parts[1])
    elif opcode == "DELETEFOLDER":
        os.rmdir(parts[1])
    elif opcode == "SWAPMEM":
        mem.mem, mem2.mem = mem2.mem, mem.mem
    elif opcode == "CHOICE-1":
        mem.push(random.choice(parts[1:]))
    elif opcode == "CHOICE-2":
        nums = [mem.pop() for _ in range(int(parts[1]))]
        mem.push(random.choice(nums))
    elif opcode == "RANDINT":
        mem.push(random.randint(int(parts[1]), int(parts[2])))
    elif opcode == "RANDOM":
        mem.push(random.random() * float(parts[1]))
    elif opcode == "SYSTEM":
        os.system(parts[1])
    elif opcode == "OUTV":
        print(mem.top())
    else:
        if not opcode.endswith(":"):
            print(f"Unrecognized opcode: {opcode}")

# Main logic
readfunc()
while program_counter < len(main_code):
    execute(main_code[program_counter])
    if not jump_occurred:
        program_counter += 1
