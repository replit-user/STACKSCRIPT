from sys import argv,exit
from collections import defaultdict
import os
import random
functions = defaultdict(list)
program_counter = 0
PATH = argv[1]
SIZE = 30000
with open(PATH,"r") as f:
    CODE = f.read().splitlines()



class stack:
    def __init__(self,size):
        self.mem = [0 for i in range(size)]
        self.pointer = 0
    def push(self,num):
        try:
            if not "." in num:
                num = int(num)
            else:
                num = float(num)

        except TypeError:
            print("not a number")
        self.mem[self.pointer] = num
        self.pointer += 1
    def pop(self):
        self.pointer -= 1
        return self.mem[self.pointer + 1]
    def top(self):
        return self.mem[self.pointer - 1]


class secondarstack:
    def __init__(self,size):
        self.mem = [0 for i in range(size)]
        self.pointer = 0
    def push(self,num):
        try:
            if not "." in num:
                num = int(num)
            else:
                num = float(num)
        except ValueError:
            print("not a number")
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
        num = input("enter a number: ")
        if "." in num:
            try:
                num = float(num)
            except ValueError:
                print("must be a number")
                exit()
            mem.push(num)
        else:
            try:
                num = int(num)
            except ValueError:
                print("must be a number")
                exit()
        mem.push(num)
    elif opcode.startswith("JMP"):
        target = int(parts[1]) - 1
        condition_met = False

        if opcode == "JMP":
            condition_met = True
        elif opcode == "JMP.EQ" and mem.top() == float(parts[2]):
            condition_met = True
        elif opcode == "JMP.GT" and mem.top() < float(parts[2]):
            condition_met = True
        elif opcode == "JMP.LT" and mem.top() > float(parts[2]):
            condition_met = True
        elif opcode == "JMP.GTE" and mem.top() <= float(parts[2]):
            condition_met = True
        elif opcode == "JMP.LTE" and mem.top() >= float(parts[2]):
            condition_met = True

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
        result = {
            "ADD": a + b,
            "SUB": a - b,
            "MUL": a * b,
            "DIV": a / b,
            "EXP": a ** b
        }[opcode]
        mem.push(result)
    elif opcode == "OUT":
        print(parts[1:])
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
    elif opcode == "SREAD":
        num = input("enter a number: ")
        if "." in num:
            try:
                num = float(num)
            except ValueError:
                print("must be a number")
                exit()
            mem.push(num)
        else:
            try:
                num = int(num)
            except ValueError:
                print("must be a number")
                exit()
        mem2.push(num)
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
    else:
        print(f"unrecognized opcode: {opcode}")
        exit()


#main logic
readfunc()
while program_counter < len(CODE):
    execute(CODE[program_counter])
    if not jump_occurred:
        program_counter += 1
