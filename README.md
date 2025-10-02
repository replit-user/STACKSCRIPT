# STACKSCRIPT Interpreter

STACKSCRIPT is a custom stack-based scripting language interpreter implemented in Python. It supports two stacks, modular programming, file and folder operations, random operations, conditional jumps, and arithmetic operations. It is designed for scripting with simple stack-based logic and modularity.

---

## Features

- **Two stacks:** Primary (`mem`) and secondary (`mem2`) for flexible stack operations.
- **Modular functions:** Functions can be defined, called, and organized into modules.
- **File system operations:** Read, write, append, delete files and folders.
- **Conditional jumps:** `JMP`, `JMPGT`, `JMPLT`, `JMPEQ`.
- **Arithmetic operations:** `ADD`, `SUB`, `MUL`, `DIV`, `EXP`.
- **Randomness:** `RANDINT`, `RANDOM`, `CHOICE-1`, `CHOICE-2`.
- **Input and output:** `READ`, `SPREAD`, `OUT`, `OUTV`, `SPOUTV`.
- **System integration:** Execute shell commands via `SYSTEM`.
- **Debugging:** Optional debug mode with breakpoints.

---

## Installation

1. Clone or download the repository.
2. Ensure Python 3.8+ is installed.
3. Run STACKSCRIPT files using Python:

```bash
python stackscript.py --path example.stack
```

---

## Command-Line Arguments

-   `--path` or `-p` : Path to the STACKSCRIPT file to execute.
    
-   `--debug` or `-d` : Enable debug mode (prints stack, variables, and program counter).
    
-   `--version` or `-v` : Show interpreter version.
    
-   Additional arguments after the script are passed as `%ARG<n>` variables to the script.
    

Example:

```bash
python stackscript.py -p myscript.stack 42 "hello"
```

In the script:

-   `%VAR<%ARG1>` → `42`
    
-   `%VAR<%ARG2>` → `"hello"`
    

---

## STACKSCRIPT Syntax

### Functions

```text
function_name:
    PUSH 10
    PUSH 20
    ADD
ENDFUNC
```

-   Functions are declared with a trailing colon (`:`) and terminated by `ENDFUNC`.
    
-   Call with `CALL function_name`.
    

### Modules

-   Modules are stored in `.stack` and `.stackm` files.
    
-   Exported functions are declared in `.stackm` using:
    

```text
EXTERN func1 func2
```

-   Load modules using:
    

```text
LOAD module_name
CALL module_name.func1
```

---

## Opcodes Overview

| Opcode | Description |
| --- | --- |
| `PUSH <num>` | Push number to primary stack. |
| `POP` | Pop from primary stack. |
| `TOP` | Duplicate the top of the primary stack. |
| `DUP` | Push the top of secondary stack to primary stack. |
| `SPUSH <num>` | Push number to secondary stack. |
| `PUD` | Push top of primary stack to secondary stack. |
| `SWAP <a> <b>` | Swap values in primary stack. |
| `S-SWAP <a> <b>` | Swap values in secondary stack. |
| `BOTOP` | Push bottom value of primary stack. |
| `CLEAR` | Reset primary stack. |
| `SWAPMEM` | Swap primary and secondary stacks. |
| `ADD`, `SUB`, `MUL`, `DIV`, `EXP` | Arithmetic on top two elements of primary stack. |
| `OUT <text>` | Print text to console. |
| `OUTV` | Print top of primary stack. |
| `SPOUTV` | Print top of secondary stack. |
| `READ` | Read number from input into primary stack. |
| `SPREAD` | Read number from input into secondary stack. |
| `JMP <line>` | Unconditional jump. |
| `JMPGT <val> <line>` | Jump if top of stack > val. |
| `JMPLT <val> <line>` | Jump if top of stack < val. |
| `JMPEQ <val> <line>` | Jump if top of stack == val. |
| `CALL <func>` | Call a function (optionally module-qualified). |
| `SET <var> <val>` | Assign value to a variable. |
| `LOAD <module>` | Load a module (`.stack` + `.stackm`). |
| `SYSTEM <command>` | Run shell command. |
| `READFILE <file>` | Print contents of a file. |
| `WRITEFILE <file> <text>` | Write text to a file. |
| `APPENDFILE <file> <text>` | Append text to a file. |
| `DELETEFILE <file>` | Delete a file. |
| `CREATEFILE <file> <text>` | Create a file with initial text. |
| `CREATEFOLDER <folder>` | Create a folder. |
| `DELETEFOLDER <folder>` | Delete a folder. |
| `RANDINT <a> <b>` | Push a random integer `[a,b]`. |
| `RANDOM <max>` | Push a random float `[0,max)`. |
| `CHOICE-1 <items...>` | Push random choice from items. |
| `CHOICE-2 <count>` | Push random choice from last `<count>` stack elements. |
| `HALT` | Stop execution. |
| `BREAKPOINT` | Pause for debugging (only in debug mode). |

---

## Variables

-   Variables are declared dynamically with `SET`.
    
-   Access via `%VAR<varname>` or `%VAR<%ARGn>` for script arguments.
    
-   `last_pop` stores the value of the last `POP`.
    

---

## Example STACKSCRIPT File

```text
PUSH 5
PUSH 10
ADD
OUTV
```

Output:

```
15
```

Example with a function:

```text
sum:
    PUSH 5
    PUSH 10
    ADD
ENDFUNC

CALL sum
OUTV
```

---

## Debugging

Run with `--debug` to:

-   Print program counter, variables, stacks, and executed instructions.
    
-   Use `BREAKPOINT` opcode to pause execution.
    
