from sys import exit
from collections import defaultdict
import os
import random
from typing import Optional
from argparse import ArgumentParser
import re

# --- ARGUMENT PARSING ---
parser = ArgumentParser(description="STACKSCRIPT Interpreter")
parser.add_argument("--path","-p", type=str, help="Path to the STACKSCRIPT file")
parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
parser.add_argument("-v", "--version", action="version", version="%(prog)s 3.0", help="Show version and exit")
parser.add_argument("args", nargs="*", help="the arguments to pass to the script")
args = parser.parse_args()
if args.debug:
    print("Debug mode enabled")

SCRIPT_ARGS = args.args
SCRIPT_ARGS.insert(0,args.path)

functions = defaultdict(list)
modules = defaultdict(dict)
exported_functions = defaultdict(set)
program_counter = 0
variables = defaultdict(lambda: 0)
PATH = args.path
SIZE = 30000
loop_stack = []  # Track named loops (FOR, WHILE, IF)

# --- INITIALIZE ARG VARIABLES ---
for i, arg in enumerate(SCRIPT_ARGS):
    try:
        val = float(arg) if '.' in arg else int(arg)
    except ValueError:
        val = arg
    variables[f"%ARG{i}"] = val

# --- LOAD SCRIPT ---
with open(PATH, "r") as f:
    CODE = f.read().splitlines()

main_code = []

# --- STACK CLASSES ---
class stack:
    def __init__(self, size):
        self.mem = [0]*size
        self.pointer = 1
    def push(self, val):
        self.mem[self.pointer] = val
        self.pointer += 1
    def pop(self):
        self.pointer -= 1
        variables["last_pop"] = self.mem[self.pointer]
        return self.mem[self.pointer]
    def top(self):
        return self.mem[self.pointer-1]

class secondarstack:
    def __init__(self, size):
        self.mem = [0]*size
        self.pointer = 1
    def push(self, val):
        self.mem[self.pointer] = val
        self.pointer += 1
    def top(self):
        return self.mem[self.pointer-1]

mem = stack(SIZE)
mem2 = secondarstack(SIZE)
jump_occurred = False

# --- PARSE FUNCTIONS ---
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

# --- HELPER: VARIABLE REPLACEMENT ---
def replace_vars(expr):
    def repl_var(match):
        var_name = match.group(1)
        val = variables.get(var_name, 0)
        if isinstance(val,str):
            return f'"{val}"'
        return str(val)
    return re.sub(r"%VAR<([^>]+)>", repl_var, expr)

# --- EXECUTE INSTRUCTION ---
def execute(instruction: str, current_module: Optional[str] = None):
    global mem, mem2, jump_occurred, program_counter, loop_stack
    jump_occurred = False
    parts = instruction.strip().split()
    if not parts:
        return
    opcode = parts[0]

    # --- COMMENT IGNORE ---
    if ";" in instruction:
        execute(instruction.split(";")[0].strip())
        return

    # --- STACK OPERATIONS ---
    if opcode in {"READ","SPREAD"}:
        val = input("Enter a value: ").strip()
        try: val = float(val) if '.' in val else int(val)
        except: pass
        if opcode=="READ": mem.push(val)
        else: mem2.push(val)

    elif opcode in {"PUSH","SPUSH"}:
        value = " ".join(parts[1:])
        try: value = float(value) if '.' in value else int(value)
        except: pass
        if opcode=="PUSH": mem.push(value)
        else: mem2.push(value)

    elif opcode=="POP": mem.pop()
    elif opcode=="HALT": exit()
    elif opcode in {"ADD","SUB","MUL","DIV","EXP"}:
        b=mem.pop();a=mem.pop()
        if isinstance(a,str) or isinstance(b,str):
            mem.push(str(a)+str(b) if opcode=="ADD" else "")
        else:
            if opcode=="ADD": mem.push(a+b)
            elif opcode=="SUB": mem.push(a-b)
            elif opcode=="MUL": mem.push(a*b)
            elif opcode=="DIV": mem.push(0 if b==0 else a/b)
            elif opcode=="EXP": mem.push(a**b)

    elif opcode=="OUT": print(" ".join(parts[1:]))
    elif opcode=="OUTV": print(mem.top())
    elif opcode=="BOTOP": mem.push(mem.mem[0])
    elif opcode=="CLEAR": mem=stack(SIZE)
    elif opcode=="SET": variables[parts[1]] = float(parts[2]) if '.' in parts[2] else int(parts[2])

    # --- CONDITIONALS ---
    elif opcode in {"IF","ELIF"}:
        cond_expr = replace_vars(" ".join(parts[1:]))
        try: result = eval(cond_expr)
        except Exception as e: print(f"Error evaluating '{cond_expr}': {e}"); exit()
        if opcode=="IF": loop_stack.append(("IF", result))
        elif opcode=="ELIF":
            if not loop_stack or loop_stack[-1][0]!="IF": print("ELIF without IF"); exit()
            prev_result=loop_stack[-1][1]
            result = result and not prev_result
            loop_stack[-1]=("IF", prev_result or result)
        if not result:
            depth=1
            while depth>0 and program_counter+1<len(main_code):
                program_counter+=1
                line=main_code[program_counter].strip()
                if line.startswith("IF"): depth+=1
                elif line.startswith(("ELSE","ELIF")) and depth==1: break
                elif line.startswith("ENDIF"): depth-=1
            jump_occurred=True

    elif opcode=="ELSE":
        depth=1
        while depth>0 and program_counter+1<len(main_code):
            program_counter+=1
            line=main_code[program_counter].strip()
            if line.startswith("IF"): depth+=1
            elif line.startswith("ENDIF"): depth-=1
        jump_occurred=True

    elif opcode=="ENDIF":
        if loop_stack and loop_stack[-1][0]=="IF": loop_stack.pop()

    # --- FOR LOOP ---
    elif opcode=="FOR":
        loop_name = parts[1]
        var_name = parts[2]
        start=int(parts[3]); end=int(parts[4])
        step=int(parts[5]) if len(parts)>5 else 1
        variables[var_name]=start
        # find END loop
        depth=1; pc=program_counter
        while depth>0:
            pc+=1
            line=main_code[pc].strip()
            if line.startswith(f"FOR {loop_name}"): depth+=1
            elif line.startswith(f"END {loop_name}"): depth-=1
        loop_stack.append(("FOR", loop_name, program_counter, pc, var_name, step, end))

    elif opcode=="WHILE":
        loop_name = parts[1] if len(parts)>1 else f"WHILE{program_counter}"
        cond_expr = replace_vars(" ".join(parts[1:]))
        try: result = eval(cond_expr)
        except Exception as e: print(f"Error evaluating WHILE '{cond_expr}': {e}"); exit()
        # find END loop
        depth=1; pc=program_counter
        while depth>0:
            pc+=1
            line=main_code[pc].strip()
            if line.startswith("WHILE"): depth+=1
            elif line.startswith(f"END {loop_name}"): depth-=1
        if result: loop_stack.append(("WHILE", loop_name, program_counter, pc, cond_expr))
        else: program_counter=pc; jump_occurred=True

    elif opcode.startswith("END"):
        loop_name = parts[1] if len(parts)>1 else None
        if not loop_stack: print("END used outside loop"); exit()
        top = loop_stack[-1]; ltype=top[0]; lname=top[1]
        if loop_name!=lname: print(f"END {loop_name} does not match {lname}"); exit()
        if ltype=="FOR":
            _,_,start_pc,end_pc,var_name,step,end_val=top
            variables[var_name]+=step
            if (step>0 and variables[var_name]<=end_val) or (step<0 and variables[var_name]>=end_val):
                program_counter=start_pc
            else: loop_stack.pop()
            jump_occurred=True
        elif ltype=="WHILE":
            _,_,start_pc,end_pc,cond_expr=top
            try:
                if eval(replace_vars(cond_expr)): program_counter=start_pc
                else: loop_stack.pop()
            except Exception as e: print(f"Error evaluating WHILE '{cond_expr}': {e}"); exit()
            jump_occurred=True

    elif opcode=="BREAK":
        if not loop_stack: print("BREAK used outside loop"); exit()
        top=loop_stack.pop()
        _,_,_,end_pc,*rest=top
        program_counter=end_pc
        jump_occurred=True

# --- MAIN EXECUTION ---
readfunc()
while program_counter<len(main_code):
    execute(main_code[program_counter])
    if args.debug and not main_code[program_counter].startswith("CALL"):
        print(f"variables: {variables}, PC:{program_counter+1}, Stack:{mem.mem[:mem.pointer]}, Stack2:{mem2.mem[:mem2.pointer]}, Instruction:{main_code[program_counter]}")
    if not jump_occurred:
        program_counter+=1
