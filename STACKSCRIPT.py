from sys import argv
from collections import defaultdict
import os
import random
path = argv[1]


with open(path,"r") as f:
    program = f.readlines()
    i = 0
    for line in program:
        program[i] = line.strip()
        i += 1


functions = defaultdict(list)


currentfunc = None


index = 0


jump_occured = False




path = argv[1]


class stack:
    def __init__(self,size):
        self.size = size
        self.mem = [0 for _ in range(self.size)]
        self.pointer = 0
    def pop(self):
        number = self.mem[self.pointer]
        self.mem[self.pointer] = 0
        self.pointer -= 1
        return number
    def push(self,number:float|int):
        try:
            number = float(number)
        except ValueError:
            print("not a number")
            exit()
        self.pointer += 1
        self.mem[self.pointer] = number
    def top(self):
        return self.mem[self.pointer]
   






class secondstack:
    def __init__(self,size):
        self.size = size
        self.mem = [0 for _ in range(size)]
        self.pointer = 0
    def push(self,num):
        self.pointer += 1
        self.mem[self.pointer] = num








mem = stack(500000)
mem2 = secondstack(500000)








def execute(instruction:str):
    if ";" in instruction:
        instr = instruction.split(";")[0]
        execute(instr)
    global jump_occured,index,currentfunc
    parts = instruction.split(" ")
    opcode = parts[0]
    if opcode == "READ":
        number = input("enter a number: ")
        if "." in number:
            try:
                number = float(number)
                mem.push(number)
            except ValueError:
                print("not a number")
        else:
            try:
                number = int(number)
                mem.push(number)
            except ValueError:
                print("not a number")
    elif opcode == "JMP" and currentfunc is None:
        jump_occured = True
        index = int(parts[1])
    elif opcode == "JMP.EQ" and currentfunc is None:
        if mem.top() == float(parts[2]):
            index = int(parts[1])
            jump_occured = True
        else:
            jump_occured = False
    elif opcode == "JMP.GT" and currentfunc is None:
        if mem.top() < float(parts[2]):
            index = int(parts[1])
            jump_occured = True
        else:
            jump_occured = False
    elif opcode == "JMP.LT" and currentfunc is None:
        if mem.top() > float(parts[2]):
            index = int(parts[1])
            jump_occured = True
        else:
            jump_occured = False
    elif opcode == "JMP.GTE" and currentfunc is None:
        if mem.top() <= float(parts[2]):
            index = int(parts[1])
            jump_occured = True
        else:
            jump_occured = False
    elif opcode == "JMP.LTE" and currentfunc is None:
        if mem.top() >= float(parts[2]):
            index = int(parts[1])
            jump_occured = True
        else:
            jump_occured = False
    elif opcode == "PUSH" and currentfunc == None:
        mem.push(parts[1])
    elif opcode == "POP" and currentfunc == None:
        mem.pop()
    elif opcode == "HALT":
        if currentfunc == None:
            jump_occured = False
            exit()
        else:
            currentfunc = None
    elif opcode in ["ADD","SUB","DIV","MUL","EXP"] and currentfunc == None:
        jump_occured = False
        a = mem.pop()
        b = mem.pop()
        if opcode == "ADD":
            mem.push(a + b)
        elif opcode == "SUB":
            mem.push(a - b)
        elif opcode == "MUL":
            mem.push(a * b)
        elif opcode == "DIV":
            mem.push(a / b)
        elif opcode == "EXP":
            mem.push(a ** b)
    elif opcode == "OUT" and currentfunc is None:
        print(" ".join(parts[1:]))
    elif opcode == "OUTV" and currentfunc is None:
        print(mem.top())
    elif opcode == "BOTOP":
        mem.push(mem.mem[0])
    elif opcode == "CLEAR":
        mem.mem = [0 for i in range(mem.size)]
        mem.pointer = 0
    elif ":" in opcode:
        functions[opcode.replace(":","")] = []
        currentfunc = opcode.replace(":","")
    elif opcode == "CALL":
        for instruct in functions[parts[1]]:
            execute(instruct)
    elif opcode == "ENDFUNC":
        jump_occured = False
        currentfunc = None
    elif opcode == "COPY":
        mem.push(mem.mem[int(parts[1])])
    elif opcode == "DUP":
        mem.push(mem2.mem[mem2.pointer])
    elif opcode == "SPUSH":
        mem2.push(float(parts[1]))
    elif opcode == "SPREAD":
        try:
            number = float(input("enter a number: "))
            execute(f"SPUSH {number}")
        except ValueError as e:
            print("not a valid number: " + e)
    elif opcode == "PUD":
        mem2.push(mem.top())
    elif opcode == "SWAP":
        mem.mem[int(parts[1])] = int(parts[2])
        mem.mem[int(parts[2])] = int(parts[1])
    elif opcode == "READFILE":
        with open(parts[1],"r") as f:
            text = f.read()
            print(text)
    elif opcode == "WRITEFILE":
        with open(parts[1],"w") as f:
            f.write(parts[2:])
    elif opcode == "APPENDFILE":
        with open(parts[1],"a") as f:
            f.write(parts[2])
    elif opcode == "DELETEFILE":
        os.system(f"rm {parts[1]}")
    elif opcode == "CREATEFILE":
        os.system(f"echo {parts[2]} >> {parts[1]}")
    elif opcode == "CREATEFOLDER":
        os.mkdir(parts[1])
    elif opcode == "DELETEFOLDER":
        os.rmdir(parts[1])
    elif opcode == "SWAPMEM":
        mem1 = mem.mem
        mem3 = mem2.mem
        mem.mem = mem3
        mem2.mem = mem1
    elif opcode == "RANDINT":
        mem.push(random.randint(parts[1],parts[2]))
    elif opcode == "RANDOM":
        mem.push(random.random() * parts[1])
    elif opcode == "SYSTEM":
        os.system(parts[1])
    if currentfunc is not None:
        functions[currentfunc].append(instruction)
while index <= len(program) - 1:
    execute(program[index])
    if not jump_occured:
        index += 1


