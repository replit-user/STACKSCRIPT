# STACKSCRIPT

STACKSCRIPT is a stack-based scripting language designed for low-level control of memory and functions. Instructions are written in uppercase and processed line-by-line, with support for user-defined functions, file manipulation, and random number generation.

---

## Memory

STACKSCRIPT uses two memory stacks:
- **Primary stack** (`mem`): General-purpose memory.
- **Secondary stack** (`mem2`): Auxiliary memory.

---

## Instructions

### Stack Operations
- **PUSH x**: Push value `x` onto the primary stack.
- **POP**: Pop (remove) the top value from the primary stack.
- **SPUSH x**: Push value `x` onto the secondary stack.
- **PUD**: Push the top value from the primary stack onto the secondary stack.
- **TOP**: Push a copy of the top value from the primary stack onto the primary stack.
- **DUP**: Push the top value from the secondary stack onto the primary stack.
- **COPY addr**: Push the value at memory address `addr` from the primary stack.
- **SWAP addr1 addr2**: Swap the values at addresses `addr1` and `addr2` in the primary stack.
- **S-SWAP addr1 addr2**: Swap the values at addresses `addr1` and `addr2` in the secondary stack.
- **BOTOP**: Push the value at address 0 of the primary stack onto the top.
- **CLEAR**: Clear the primary stack (reset).
- **SWAPMEM**: Swap the entire contents and pointers of `mem` and `mem2`.

### Input/Output
- **READ**: Prompt the user for input and push it to the primary stack.
- **SPREAD**: Prompt the user for input and push it to the secondary stack.
- **OUT text**: Output the given text.
- **OUTV**: Output the top value of the primary stack.
- **SPOUTV**: Output the top value of the secondary stack.

### Math Operations
- **ADD**: Pop two values, add them, push the result.
- **SUB**: Pop two values, subtract the second from the first, push the result.
- **MUL**: Pop two values, multiply them, push the result.
- **DIV**: Pop two values, integer divide first by second, push the result.
- **EXP**: Pop two values, raise the first to the power of the second, push the result.

### Control Flow
- **JMP line**: Jump to a specific line number.
- **JMPEQ x line**: Jump if the top value equals `x`.
- **JMPGT x line**: Jump if the top value is greater than `x`.
- **JMPLT x line**: Jump if the top value is less than `x`.
- **HALT**: Stop program execution.

### Functions
- **funcname:**: Define a new function.
- **ENDFUNC**: End function definition.
- **CALL funcname**: Call a function.

### File Operations
- **READFILE filename**: Read and output the contents of a file.
- **WRITEFILE filename content...**: Write content to a file (overwrites).
- **APPENDFILE filename content...**: Append content to a file.
- **DELETEFILE filename**: Delete a file.
- **CREATEFILE filename content...**: Create a file with the given content.
- **CREATEFOLDER foldername**: Create a folder.
- **DELETEFOLDER foldername**: Delete a folder.

### Randomness
- **CHOICE-1 val1 val2 val3 ...**: Push a random choice from the given values.
- **CHOICE-2 n**: Randomly pick one value from the top `n` popped values.
- **RANDINT min max**: Push a random integer between `min` and `max`.
- **RANDOM scale**: Push a random floating-point number between `0` and `scale`.

### System
- **SYSTEM command**: Run a system command (OS shell).

### Error Handling
- Unknown instructions print an error: `Unrecognized opcode: OPCODE`

---

## Example Program
```plaintext
OUT Hello World!
PUSH 5
PUSH 10
ADD
OUTV
HALT
```

---

## License
STACKSCRIPT is an open, educational project for learning about stack-based scripting and interpreter design.

---

## Notes
- Lines can contain multiple instructions separated by `;` (semicolon).
- Whitespace is ignored around commands.
- Function names must end with `:`.

Happy STACKSCRIPTING!

