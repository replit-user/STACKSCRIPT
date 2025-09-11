
# STACKSCRIPT

[](LICENSE)

[](LICENSE)

**STACKSCRIPT** is a custom, stack-based programming language designed for educational and experimental purposes. It features dual stacks, modular scripting, and direct file & system operations.

---

## Features

-   **Stack-based execution**: Primary and secondary stacks (`mem` and `mem2`) for advanced data manipulation.
    
-   **Arithmetic operations**: `ADD`, `SUB`, `MUL`, `DIV`, `EXP`.
    
-   **Control flow**: Conditional and unconditional jumps (`JMP`, `JMPGT`, `JMPLT`, `JMPEQ`).
    
-   **Input/Output**: `READ`, `SPREAD`, `OUT`, `OUTV`, `SPOUTV`.
    
-   **File operations**: `READFILE`, `WRITEFILE`, `APPENDFILE`, `DELETEFILE`, `CREATEFILE`, `CREATEFOLDER`, `DELETEFOLDER`.
    
-   **Randomization**: `RANDINT`, `RANDOM`, `CHOICE-1`, `CHOICE-2`.
    
-   **Module system**: Load `.stack` and `.stackm` modules with `LOAD` and call exported functions across modules.
    
-   **Debugging**: `BREAKPOINT` shows stack and variable states when `--debug` is enabled.
    
-   **System interaction**: Run system commands with `SYSTEM`.
    

---

## Installation

1.  Clone the repository:
    
    ```bash
    git clone https://github.com/yourusername/stackscripts.git
    ```
    
2.  Ensure you have Python 3.10+ installed.
    
3.  Run your `.stack` scripts using the interpreter:
    
    ```bash
    python stackscript.py --path your_script.stack [args...] [--debug]
    ```
    

---

## Getting Started

1.  **Create a STACKSCRIPT file**:
    

```stack
PUSH 5
PUSH 10
ADD
OUTV         ; Prints 15
HALT
```

2.  **Run the script**:
    

```bash
python stackscript.py --path example.stack
```

3.  **Passing arguments**:
    

```stack
; Access arguments via %ARG0, %ARG1, etc.
OUT %ARG0
```

```bash
python stackscript.py --path example.stack Hello World
```

Output:

```nginx
Hello
```

4.  **Debug mode**:
    

```bash
python stackscript.py --path example.stack --debug
```

This prints variable states, program counter, and stack contents at each step.

---

## Opcode Reference

| Opcode | Description |
| --- | --- |
| `PUSH <num>` | Push a number onto the primary stack. |
| `POP` | Remove the top element of the primary stack. |
| `TOP` | Duplicate the top value of the primary stack. |
| `BOTOP` | Push the bottom value of the primary stack to the top. |
| `DUP` | Push the top value of the secondary stack onto the primary stack. |
| `SPUSH <num>` | Push a number onto the secondary stack. |
| `PUD` | Push the top value of the primary stack onto the secondary stack. |
| `SWAP <a> <b>` | Swap values at two indices in the primary stack. |
| `S-SWAP <a> <b>` | Swap values at two indices in the secondary stack. |
| `ADD` | Pop two values from the primary stack, add, and push result. |
| `SUB` | Pop two values from the primary stack, subtract, and push result. |
| `MUL` | Pop two values from the primary stack, multiply, and push result. |
| `DIV` | Pop two values from the primary stack, divide, and push result (0 if divide by 0). |
| `EXP` | Pop two values from the primary stack, exponentiate, and push result. |
| `READ` | Read user input as number and push to primary stack. |
| `SPREAD` | Read user input as number and push to secondary stack. |
| `OUT <text>` | Print text. |
| `OUTV` | Print the top value of the primary stack. |
| `SPOUTV` | Print the top value of the secondary stack. |
| `JMP <line>` | Unconditional jump to line number. |
| `JMPGT <val> <line>` | Jump if top of primary stack > val. |
| `JMPLT <val> <line>` | Jump if top of primary stack < val. |
| `JMPEQ <val> <line>` | Jump if top of primary stack == val. |
| `CALL <func>` | Call a function from the current module or loaded module. |
| `LOAD <module>` | Load a `.stack` module and its exports. |
| `SET <var> <val>` | Define a variable in memory. |
| `COPY <addr>` | Copy value from memory address onto the primary stack. |
| `CLEAR` | Reset primary stack. |
| `SWAPMEM` | Swap primary and secondary stacks. |
| `CHOICE-1 <options>` | Push a random value from listed options. |
| `CHOICE-2 <n>` | Pop `n` values from primary stack and push a random one. |
| `RANDINT <min> <max>` | Push random integer in range. |
| `RANDOM <max>` | Push random float in range `[0, max)`. |
| `SYSTEM <cmd>` | Execute system command. |
| `READFILE <file>` | Print file contents. |
| `WRITEFILE <file> <text>` | Overwrite file with text. |
| `APPENDFILE <file> <text>` | Append text to file. |
| `DELETEFILE <file>` | Delete a file. |
| `CREATEFILE <file> <text>` | Create a new file with text. |
| `CREATEFOLDER <folder>` | Create a new folder. |
| `DELETEFOLDER <folder>` | Delete a folder. |
| `HALT` | Stop execution. |
| `BREAKPOINT` | Pause execution in debug mode. |

---

## Modules

-   Modules are `.stack` and `.stackm` files.
    
-   `.stackm` contains `EXTERN func1 func2 ...` for exported functions.
    
-   Call cross-module functions:
    

```stack
CALL module.func
```

---

## Contributing

STACKSCRIPT is open for modification, experimentation, and learning. Please follow the **Responsible Sharing License v1.0 (RSL 1.0)** for contributions and redistributions.

---

## License

This project is licensed under the **Responsible Sharing License v1.0**.  
Please see the [LICENSE](LICENSE) file for full details.

---
    

---
