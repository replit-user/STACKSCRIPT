

# STACKSCRIPT

STACKSCRIPT is a minimalist, stack-based scripting language with two memory stacks and function support. It is interpreted using Python and designed for low-level manipulation, basic file I/O, math, conditional jumps, and simple user interactions.

---

## 🔧 Running a STACKSCRIPT Program

To run a script:

```bash
python3 interpreter.py yourscript.stack
```

Replace `interpreter.py` with the filename of the interpreter, and `yourscript.stack` with your STACKSCRIPT file.

---

## 📚 Language Overview

### ▶️ Execution Model

* Code is executed line by line.
* Functions can be defined and called using `CALL`.
* Two stack memories (`mem` and `mem2`) are available for storage.
* **Semicolons (`;`) denote line comments** — anything after a `;` on a line is ignored.

### 📦 Stacks

* **Primary stack (`mem`)**: General use.
* **Secondary stack (`mem2`)**: Often used for auxiliary storage.

---

## 🔤 Instructions Reference

### I/O

* `READ` — Input a number into `mem`.
* `SPREAD` — Input a number into `mem2`.
* `OUT <text>` — Print literal text.
* `OUTV` — Print the top of `mem`.
* `SPOUTV` — Print the top of `mem2`.

### Stack Ops

* `PUSH <value>` — Push value onto `mem`.
* `POP` — Remove top of `mem`.
* `TOP` — Duplicate top of `mem`.
* `DUP` — Push top of `mem2` to `mem`.
* `SPUSH <value>` — Push value to `mem2`.
* `PUD` — Push top of `mem` to `mem2`.
* `COPY <addr>` — Push value from `mem[addr]`.
* `SWAP <addr1> <addr2>` — Swap values in `mem`.
* `S-SWAP <addr1> <addr2>` — Swap values in `mem2`.
* `BOTOP` — Push `mem[0]` to top of `mem`.
* `CLEAR` — Clear the `mem` stack.
* `SWAPMEM` — Swap `mem` with `mem2`.

### Math

* `ADD`, `SUB`, `MUL`, `DIV`, `EXP`

### Control Flow

* `JMP <line>` — Jump unconditionally.
* `JMPGT <value> <line>` — Jump if top of `mem` > value.
* `JMPLT <value> <line>` — Jump if top of `mem` < value.
* `JMPEQ <value> <line>` — Jump if top of `mem` == value.
* `HALT` — Stop execution.

### Functions

Define functions using:

```stack
myFunction:
  PUSH 5
  ADD
ENDFUNC
```

Call with:

```
CALL myFunction
```

### Filesystem

* `READFILE <filename>` — Print file contents.
* `WRITEFILE <filename> <text...>` — Write text to file.
* `APPENDFILE <filename> <text...>` — Append text.
* `CREATEFILE <filename> <text...>` — Create a new file.
* `DELETEFILE <filename>` — Delete file.
* `CREATEFOLDER <foldername>` — Create a folder.
* `DELETEFOLDER <foldername>` — Remove folder.

### Randomness

* `CHOICE-1 <val1> <val2> ...` — Push a random argument.
* `CHOICE-2 <count>` — Pop `count` values from `mem`, push a random one.
* `RANDINT <min> <max>` — Push random int.
* `RANDOM <float>` — Push float in range `[0, float)`.

### System

* `SYSTEM <command>` — Execute shell command.

---

## 📝 Example

```stack
PUSH 10
PUSH 20
ADD
OUTV ; prints 30
```

---

## 📎 Notes

* All stack values are integers or floats.
* Invalid inputs halt the program.
* Function names must end with `:` and be terminated with `ENDFUNC`.
* Semicolons (`;`) **comment out the rest of the line**, similar to `//` in other languages.

---

## 📂 File Structure

* `.stack` — Your STACKSCRIPT source files.
* Interpreter is a single `.py` file.

---

## 🔚 License

none, just do what you want as long its its legal, idc

---

## 🙋‍♂️ Contributing

Pull requests are welcome. Submit issues or ideas to improve STACKSCRIPT!
