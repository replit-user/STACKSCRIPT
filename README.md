# STACKSCRIPT Programming Language

STACKSCRIPT is a custom stack-based scripting language designed for educational and experimental purposes. It uses two primary stacks and supports modular code execution. This README provides an overview of the language, its syntax, and the package manager `espm`.

---

## Features

* Two-stack architecture (primary and secondary)
* Simple, linear bytecode-like instructions
* Support for modular functions and inter-module calls
* Conditional jumps and arithmetic
* I/O operations

---

## Basic Usage

```bash
python STACKSCRIPT.py path/to/code.stack
```

---

## Stack Operations

| Command | Description                 |
| ------- | --------------------------- |
| PUSH x  | Push x to the primary stack |
| POP     | Pop from the primary stack  |
| BOTOP   | Push bottom of stack to top |
| CLEAR   | Reset the primary stack     |

---

## Arithmetic

| Command | Description                   |
| ------- | ----------------------------- |
| ADD     | Pop two values, push a + b    |
| SUB     | Pop two values, push a - b    |
| MUL     | Pop two values, push a \* b   |
| DIV     | Pop two values, push a // b   |
| EXP     | Pop two values, push a \*\* b |

---

## I/O

| Command | Description                   |
| ------- | ----------------------------- |
| READ    | Read input to primary stack   |
| SPREAD  | Read input to secondary stack |
| OUT msg | Print message                 |

---

## Jumps and Flow

| Command   | Description                    |
| --------- | ------------------------------ |
| JMP x     | Jump to line x                 |
| JMPGT x y | Jump to y if top of stack > x  |
| JMPLT x y | Jump to y if top of stack < x  |
| JMPEQ x y | Jump to y if top of stack == x |
| HALT      | Terminate program              |

---

## Functions & Modules

* Define functions using `funcname:` and terminate with `ENDFUNC`
* Use `CALL funcname` or `CALL module.funcname` to call functions
* Use `EXPORT funcname` in a module to make it available externally

---

## Module System

Modules allow code reuse and separation.

* Functions defined inside modules can be selectively exported.

---

STACKSCRIPT is released under the MIT License.

---

## Author

Designed and developed for educational and sandbox computing experimentation.

