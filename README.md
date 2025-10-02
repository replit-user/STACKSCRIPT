# STACKSCRIPT

STACKSCRIPT is a simple stack-based scripting language and a Python interpreter.
Scripts execute line-by-line (top-to-bottom), similar to how Python runs a script.

Functions may be defined anywhere in the file and can be called before their definitions because the interpreter performs a pre-pass to collect all functions.

---

## Key ideas

* **No `main` function** — all top-level lines are executed in order.
* **Forward-declared functions** — functions defined later in the file are callable earlier.
* **Two stacks** — `mem` (main) and `mem2` (secondary).
* **Modules** — `.stack` source files with `.stackm` export descriptors.
* **Variable notation** — variables (including script arguments) are referenced as `%VAR<<name>>` inside scripts.

---

## Installation

Requires Python 3.8+.

```bash
git clone https://github.com/youruser/stackscript.git
cd stackscript
python stackscript.py -p examples/hello.stack
```

---

## Usage

```bash
python stackscript.py --path <script.stack> [options] [args...]
```

### Options

* `-p, --path <file>` : Path to the `.stack` script file (required).
* `-d, --debug` : Enable debug mode (prints runtime state and activates `BREAKPOINT`).
* `-v, --version` : Show interpreter version and exit.
* `args` : Extra arguments passed to the script (available as `%VAR<<ARGn>>`).

### How arguments are exposed inside scripts

When you run:

```bash
python stackscript.py -p myscript.stack foo bar
```

the interpreter populates special variables that are accessible from the script using the **`%VAR<<...>>`** notation:

* `%VAR<<ARG0>>` → the script path provided to `--path` (here: `myscript.stack`)
* `%VAR<<ARG1>>` → `foo`
* `%VAR<<ARG2>>` → `bar`

You can use these anywhere a token is read. Example:

```text
OUT "Script path:"
OUT %VAR<<ARG0>>
OUT "First user arg:"
OUT %VAR<<ARG1>>
```

**Note:** every variable (including `%VAR<<ARGn>>`) uses the same `%VAR<<name>>` notation.

---

## Variable usage

* Create a variable with `SET <name> <value>` (numbers only in the current interpreter).
* Reference variables using `%VAR<<name>>`.

Example:

```text
SET counter 10
PUSH %VAR<<counter>>
```

Substitution occurs before the instruction is executed and is token-based — the interpreter replaces tokens that exactly match the `%VAR<<name>>` pattern with their stored string value.

---

## Language reference (important opcodes)

### Stack operations

* `PUSH <num>` — push number to main stack (`mem`)
* `POP` — pop from main stack
* `TOP` — duplicate top of main stack (pushes top value)
* `BOTOP` — push value at address 0 of `mem`

### Secondary stack

* `SPUSH <num>` — push number to secondary stack (`mem2`)
* `PUD` — push main-stack top onto secondary stack
* `DUP` — push secondary-stack top onto main stack
* `SPOUTV` — print secondary-stack top

### Arithmetic

* `ADD`, `SUB`, `MUL`, `DIV`, `EXP` — binary ops: pop two operands and push the result. (`DIV` pushes `0` on divide-by-zero.)

### Control flow

* `JMP <line>` — unconditional jump to a top-level line number (1-based)
* `JMPGT <value> <line>` — jump if `mem.top() > value`
* `JMPLT <value> <line>` — jump if `mem.top() < value`
* `JMPEQ <value> <line>` — jump if `mem.top() == value`

> **Important:** line numbers used by `JMP` and relatives refer only to the *top-level instruction list* (function bodies are not counted in those line numbers).

### Functions

Define a function:

```text
myfunc:
    PUSH 10
    PUSH 20
    ADD
ENDFUNC
```

Call it with:

```text
CALL myfunc
```

Because of the pre-pass, `CALL myfunc` can appear before the `myfunc:` definition in the file.

### Modules

Modules are two files:

* `modulename.stack` — function definitions
* `modulename.stackm` — export list (lines starting with `EXTERN` list exported functions)

Load and call:

```text
LOAD mymodule
CALL mymodule.exported_func
```

Only functions listed in `EXTERN` inside `modulename.stackm` are callable from other modules.

### I/O & filesystem

* `READ` / `SPREAD` — read number into `mem` / `mem2`
* `OUT <text>` — print text
* `OUTV` — print top of `mem`
* `READFILE <file>`, `WRITEFILE <file> <text>`, `APPENDFILE <file> <text>`, `DELETEFILE <file>`, `CREATEFILE <file> <text>`
* `CREATEFOLDER <path>`, `DELETEFOLDER <path>`

### Misc

* `SYSTEM <cmd>` — run OS command
* `RANDINT <a> <b>`, `RANDOM <scale>`, `CHOICE-*` — random utilities
* `CLEAR` — reset main stack
* `SWAPMEM` — swap main and secondary stacks
* `HALT` — exit interpreter
* `SET <name> <value>` — set a variable (accessible via `%VAR<<name>>`)

---

## Execution model (how the interpreter runs your file)

1. **Pre-pass**: parse the entire file and collect all function definitions into a functions table; collect top-level lines into a separate list.
2. **Execution**: run the top-level instructions in order (line-by-line).
3. `CALL` looks up functions (current module first, then parsed functions). Forward references work because of the pre-pass.
4. `JMP` and relatives use 1-based indices into the top-level list (functions are excluded from these counts).

---

## Examples

### Example — forward call

```text
CALL hello
OUT "After call"

hello:
    PUSH 42
    OUTV
ENDFUNC
```

Output:

```
42
After call
```

### Example — using arguments

**myscript.stack**

```text
OUT "Script path:"
OUT %VAR<<ARG0>>
OUT "First arg:"
OUT %VAR<<ARG1>>
```

Run:

```bash
python stackscript.py -p myscript.stack one two
```

Output:

```
Script path:
myscript.stack
First arg:
one
```

---

## Debugging

* Run with `-d` to enable debug logging and `BREAKPOINT` support:

```bash
python stackscript.py -p script.stack -d
```

Debug prints show: `variables`, `PC` (1-based), the visible portion of both stacks, and the current instruction.

---

## Notes & caveats

* `%VAR<<name>>` is the canonical variable reference format (this includes `%VAR<<ARGn>>`).
* Substitution is token-based and done before executing an instruction.
* `JMP`/`JMPGT`/`JMPLT`/`JMPEQ` count top-level lines only; function definitions do not affect those line numbers.
* Division by zero pushes `0` instead of raising an exception.
* Module loading expects `<module>.stack` and `<module>.stackm` files to be present in the current working directory.

---

## License

MIT
