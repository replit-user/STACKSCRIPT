from sys import exit
from collections import defaultdict
import os
import random
from typing import Optional
from argparse import ArgumentParser


parser = ArgumentParser(description="StackScript Interpreter")
parser.add_argument("path", type=str, help="Path to the StackScript file")
parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
args = parser.parse_args()
if args.debug:
    print("Debug mode enabled")

functions = defaultdict(list)
modules = defaultdict(dict)  # Maps module names to their functions dict
exported_functions = defaultdict(set)  # Maps module names to exported function names
program_counter = 0
compare_slot = False
PATH = args.path
SIZE = 30000

with open(PATH, "r") as f:
    CODE = f.read().splitlines()

main_code = []

class stack:
    def __init__(self, size):
        self.mem = [0 for _ in range(size)]
        self.pointer = 1

    def push(self, num):
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
        self.mem[self.pointer] = num
        self.pointer += 1

    def top(self):
        return self.mem[self.pointer - 1]

mem = stack(SIZE)
mem2 = secondarstack(SIZE)
jump_occurred = False

def parse_code(lines):
    functions_dict = defaultdict(list)
    main_code_list = []
    in_func = False
    current_func = []
    func_name = ""
    for line in lines:
        stripped = line.strip()
        if in_func:
            if stripped == "ENDFUNC":
                in_func = False
                functions_dict[func_name] = current_func
                current_func = []
            else:
                if ':' in line:
                    if current_func:
                        functions_dict[func_name] = current_func
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
                main_code_list.append(line)
    if in_func and current_func:
        functions_dict[func_name] = current_func
    return functions_dict, main_code_list

def readfunc():
    global main_code, functions
    functions_dict, main_code_list = parse_code(CODE)
    functions = functions_dict
    main_code = main_code_list

def execute(instruction: str, current_module: Optional[str] = None) -> None:
    global mem, mem2, jump_occurred, program_counter, modules, exported_functions
    jump_occurred = False
    parts = instruction.split(" ")
    parts = [p.strip() for p in parts]
    if not parts:
        return
    opcode = parts[0]
    if ";" in instruction:
        execute(instruction.split(";")[0].strip(), current_module)
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
        if "." in parts[1]:
            mem.push(float(parts[1]))
        else:
            mem.push(int(parts[1]))
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
                mem.push(a / b)
        elif opcode == "EXP":
            mem.push(a ** b)
    elif opcode == "OUT":
        print(" ".join(parts[1:]))
    elif opcode == "BOTOP":
        mem.push(mem.mem[0])
    elif opcode == "CLEAR":
        mem = stack(SIZE)
    elif opcode == "CALL":
        func_target = parts[1]
        if '.' in func_target:
            module_name, func_name = func_target.split('.', 1)
            if module_name not in modules:
                print(f"Module {module_name} not loaded.")
                exit()
            if func_name not in modules[module_name]:
                print(f"Function {func_name} not found in module {module_name}.")
                exit()
            # Check if function is exported when called from another module
            if current_module != module_name and func_name not in exported_functions[module_name]:
                print(f"Function {module_name}.{func_name} is not exported.")
                exit()
            # Execute the function in the module's context
            for instr in modules[module_name][func_name]:
                execute(instr, module_name)
                if args.debug:
                    print(f"PC: {program_counter + 1}, Stack: {mem.mem[:mem.pointer]}, Stack2: {mem2.mem[:mem2.pointer]}, Instruction: {instr}")
        else:
            # Unqualified call, check current module first
            if current_module is not None and func_target in modules[current_module]:
                for instr in modules[current_module][func_target]:
                    execute(instr, current_module)
            elif func_target in functions:
                for instr in functions[func_target]:
                    execute(instr, current_module)
            else:
                print(f"Function {func_target} not found.")
                exit()
    elif opcode == "COPY":
        addr = int(parts[1])
        mem.push(mem.mem[addr])
    elif opcode == "DUP":
        mem.push(mem2.top())
    elif opcode == "SPUSH":
        if "." in parts[1]:
            mem2.push(float(parts[1]))
        else:
            mem2.push(int(parts[1]))
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
        mem.mem, mem.pointer, mem2.mem, mem2.pointer = mem2.mem, mem2.pointer, mem.mem, mem.pointer
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
    elif opcode == "TOP":
        mem.push(mem.top())
    elif opcode == "LOAD":
        module_name = parts[1]
        if module_name in modules:
            return
        stackm_path = f"{module_name}.stackm"
        if not os.path.exists(stackm_path):
            print(f"Module {module_name} stackm file not found.")
            exit()
        exported = []
        with open(stackm_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("EXTERN"):
                    exported.extend(line.split()[1:])
        stack_path = f"{module_name}.stack"
        if not os.path.exists(stack_path):
            print(f"Module {module_name} stack file not found.")
            exit()
        with open(stack_path, "r") as f:
            module_lines = f.read().splitlines()
        module_funcs, _ = parse_code(module_lines)
        modules[module_name] = module_funcs
        exported_functions[module_name] = set(exported)
    elif opcode == "BREAKPOINT" and args.debug:
        print(f"Breakpoint at line {program_counter + 1}: {instruction}")
        input("Press Enter to continue...")
    elif opcode == "BREAKPOINT" and not args.debug:
        None
    else:
        if not opcode.endswith(":"):
            print(f"Unrecognized opcode: {opcode}")

# Main logic
readfunc()
while program_counter < len(main_code):
    execute(main_code[program_counter])
    if args.debug and not main_code[program_counter].startswith("CALL"):
        print(f"PC: {program_counter + 1}, Stack: {mem.mem[:mem.pointer]}, Stack2: {mem2.mem[:mem2.pointer]}, Instruction: {main_code[program_counter]}")
    if not jump_occurred:
        program_counter += 1
