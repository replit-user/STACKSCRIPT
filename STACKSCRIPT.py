from sys import argv,exit
from collections import defaultdict
import os
import random
functions = defaultdict(list)
program_counter = 0
compare_slot = False
PATH = argv[1]
SIZE = 30000
with open(PATH,"r") as f:
    CODE = f.read().splitlines()



class stack:
    def __init__(self,size):
        self.mem = [0 for i in range(size)]
        self.pointer = 1
    def push(self,num):
        num = int(num)
        self.mem[self.pointer] = num
        self.pointer += 1
    def pop(self):
        self.pointer -= 1
        return self.mem[self.pointer]
    def top(self):
        return self.mem[self.pointer - 1]


class secondarstack:
    def __init__(self,size):
        self.mem = [0 for i in range(size)]
        self.pointer = 1
    def push(self,num):
        num = int(num)
        self.mem[self.pointer] = num
        self.pointer += 1
    def top(self):
        return self.mem[self.pointer - 1]


mem = stack(SIZE)
mem2 = secondarstack(SIZE)

jump_occurred = False
def readfunc():
    infunc = False
    global functions
    for instr in CODE:
        if not ":" in instr and not instr == "ENDFUNC".strip():
            if infunc == True:
                functions[func_name].append(instr)
            continue
        elif ":" in instr:
            infunc = True
            func_name = instr.replace(":","")
            functions[func_name] = []
        elif instr == "ENDFUNC".strip():
            infunc = False

def execute(instruction:str) -> None:
    global mem,mem2,jump_occurred,program_counter
    jump_occurred = False
    parts = instruction.split(" ")
    for i in range(len(parts)):
        parts[i] = parts[i].strip()
    opcode = parts[0]
    if ";" in instruction.strip():
        execute(instruction.split(";")[0])
    elif not instruction:
        return None
    elif opcode == "READ":
        num = input("Enter a number: ").strip()
        try:
            if '.' in num:  # Check if it's a float
                mem.push(float(num))  # Push as float if it contains a dot
            else:  # Otherwise, it's an integer
                mem.push(int(num))  # Push as integer
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            exit()

    elif opcode == "SPREAD":
        num = input("Enter a number: ").strip()
        try:
            if '.' in num:  # Check if it's a float
                mem2.push(float(num))  # Push as float if it contains a dot
            else:  # Otherwise, it's an integer
                mem2.push(int(num))  # Push as integer
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
                target = int(parts[2])
        elif opcode == "JMPLT":
            if mem.top() < int(parts[1]):
                condition_met = True
                target = int(parts[2])
        elif opcode == "JMPEQ":
            if mem.top() == int(parts[1]):
                condition_met = True
                target = int(parts[2])
        if condition_met:
            program_counter = target
            jump_occurred = True
        else:
            jump_occurred = False
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
            mem.push(b + a)
        elif opcode == "SUB":
            mem.push(b - a)
        elif opcode == "MUL":
            mem.push(b * a)
        elif opcode == "DIV":
            mem.push((b // (a + 1)) - 1) #insure no division by 0
        elif opcode == "EXP":
            mem.push(b ** a)
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
        num = mem.mem[int(parts[1])]
        mem.push(num)
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
        nums = []
        for i in range(int(parts[1])):
            nums.append(mem.pop())
        mem.push(random.choice(nums))
    elif opcode == "RANDINT":
        mem.push(random.randint(int(parts[1]),int(parts[2])))
    elif opcode == "RANDOM":
        mem.push(random.random() * float(parts[1]))
    elif opcode == "SYSTEM":
        os.system(parts[1])
    elif opcode == "OUTV":
        print(mem.top())
    elif not ":" in opcode:
        print(f"unrecognized opcode: {opcode}")
    else:
        None


#main logic
readfunc()
while program_counter < len(CODE):
    execute(CODE[program_counter])
    if not jump_occurred:
        program_counter += 1
