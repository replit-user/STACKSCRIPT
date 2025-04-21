from sys import argv
from collections import defaultdict
import os
import random

# Load the program
path = argv[1]
with open(path, "r") as f:
    program = [line.strip() for line in f]

# Memory Structures
class Stack:
    def __init__(self, size):
        self.size = size
        self.mem = [0] * size
        self.pointer = -1

    def push(self, value):
        try:
            value = float(value)
        except ValueError:
            print("Error: Not a number")
            exit(1)
        self.pointer += 1
        self.mem[self.pointer] = value

    def pop(self):
        if self.pointer < 0:
            print("Error: Stack underflow")
            exit(1)
        value = self.mem[self.pointer]
        self.mem[self.pointer] = 0
        self.pointer -= 1
        return value

    def top(self):
        if self.pointer < 0:
            print("Error: Stack empty")
            exit(1)
        return self.mem[self.pointer]

    def clear(self):
        self.mem = [0] * self.size
        self.pointer = -1

class SecondaryStack:
    def __init__(self, size):
        self.size = size
        self.mem = [0] * size
        self.pointer = -1

    def push(self, value):
        self.pointer += 1
        self.mem[self.pointer] = value

# Initialize memory
main_stack = Stack(500000)
secondary_stack = SecondaryStack(500000)

# Function storage
functions = defaultdict(list)
current_function = None

# Program control
program_counter = 0
jump_occurred = False

# Core execution function
def execute(instruction: str):
    global current_function, program_counter, jump_occurred

    # Handle multiple instructions on the same line
    if ";" in instruction:
        for instr in instruction.split(";"):
            execute(instr.strip())
        return

    # Ignore empty lines
    if not instruction:
        return

    parts = instruction.split()
    opcode = parts[0]

    # --- Operations ---
    if opcode == "READ":
        value = input("Enter a number: ")
        main_stack.push(value)

    elif opcode.startswith("JMP") and current_function is None:
        target = int(parts[1]) - 1
        condition_met = False

        if opcode == "JMP":
            condition_met = True
        elif opcode == "JMP.EQ" and main_stack.top() == float(parts[2]):
            condition_met = True
        elif opcode == "JMP.GT" and main_stack.top() < float(parts[2]):
            condition_met = True
        elif opcode == "JMP.LT" and main_stack.top() > float(parts[2]):
            condition_met = True
        elif opcode == "JMP.GTE" and main_stack.top() <= float(parts[2]):
            condition_met = True
        elif opcode == "JMP.LTE" and main_stack.top() >= float(parts[2]):
            condition_met = True

        if condition_met:
            program_counter = target
            jump_occurred = True
        else:
            jump_occurred = False

    elif opcode == "PUSH":
        main_stack.push(parts[1])

    elif opcode == "POP":
        main_stack.pop()

    elif opcode == "HALT":
        if current_function is None:
            exit(0)
        else:
            current_function = None

    elif opcode in {"ADD", "SUB", "MUL", "DIV", "EXP"}:
        b = main_stack.pop()
        a = main_stack.pop()
        result = {
            "ADD": a + b,
            "SUB": a - b,
            "MUL": a * b,
            "DIV": a / b,
            "EXP": a ** b
        }[opcode]
        main_stack.push(result)

    elif opcode == "OUT":
        print(" ".join(parts[1:]))

    elif opcode == "OUTV":
        print(main_stack.top())

    elif opcode == "BOTOP":
        main_stack.push(main_stack.mem[0])

    elif opcode == "CLEAR":
        main_stack.clear()

    elif ":" in opcode:
        function_name = opcode.rstrip(":")
        current_function = function_name

    elif opcode == "CALL":
        func_name = parts[1]
        for instr in functions[func_name]:
            execute(instr)

    elif opcode == "ENDFUNC":
        current_function = None

    elif opcode == "COPY":
        address = int(parts[1])
        main_stack.push(main_stack.mem[address])

    elif opcode == "DUP":
        main_stack.push(secondary_stack.mem[secondary_stack.pointer])

    elif opcode == "SPUSH":
        secondary_stack.push(float(parts[1]))

    elif opcode == "SPREAD":
        value = input("Enter a number: ")
        main_stack.push(value)

    elif opcode == "PUD":
        secondary_stack.push(main_stack.top())

    elif opcode == "SWAP":
        addr1 = int(parts[1])
        addr2 = int(parts[2])
        main_stack.mem[addr1], main_stack.mem[addr2] = main_stack.mem[addr2], main_stack.mem[addr1]

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
        main_stack.mem, secondary_stack.mem = secondary_stack.mem, main_stack.mem

    elif opcode == "RANDINT":
        main_stack.push(random.randint(int(parts[1]), int(parts[2])))

    elif opcode == "RANDOM":
        main_stack.push(random.random() * float(parts[1]))

    elif opcode == "SYSTEM":
        os.system(" ".join(parts[1:]))

    else:
        print(f"Unknown opcode: {opcode}")

    # Save function instructions if inside a function
    if current_function:
        functions[current_function].append(instruction)

# --- Main Execution Loop ---
while program_counter < len(program):
    execute(program[program_counter])
    if not jump_occurred:
        program_counter += 1
    else:
        jump_occurred = False
