## Table of Contents

1. [Introduction](#introduction)
2. [STACKSCRIPT Language Reference](#stackscript-language-reference)

   * 2.1 [Overview](#overview)
   * 2.2 [Basic Syntax and Structure](#basic-syntax-and-structure)
   * 2.3 [Data Stacks and Secondary Stack](#data-stacks-and-secondary-stack)
   * 2.4 [Core Instructions](#core-instructions)
   * 2.5 [File and I/O Operations](#file-and-io-operations)
   * 2.6 [Control Flow and Functions](#control-flow-and-functions)
   * 2.7 [Modules and Exporting](#modules-and-exporting)
   * 2.8 [Examples](#examples)
3. [ESPM Package Manager](#espm-package-manager)

   * 3.1 [Overview](#overview-1)
   * 3.2 [Commands](#commands)

     * 3.2.1 [install](#install)
     * 3.2.2 [list](#list)
     * 3.2.3 [uninstall](#uninstall)
     * 3.2.4 [upload](#upload)
   * 3.3 [File Formats: `.stack` and `.stackm`](#file-formats-stack-and-stackm)
   * 3.4 [Backend API Endpoints](#backend-api-endpoints)
   * 3.5 [Troubleshooting](#troubleshooting)
   * 3.6 [Example Workflow](#example-workflow)

---

## Introduction

This document provides a comprehensive guide for **STACKSCRIPT**, a stack-based scripting language, and **ESPM** (Experimental STACKSCRIPT Package Manager), the CLI tool and ecosystem for distributing and managing STACKSCRIPT modules. Whether you are writing automation scripts in STACKSCRIPT or publishing functions as reusable packages, this reference will help you get started and master advanced features.

## STACKSCRIPT Language Reference

### 2.1 Overview

STACKSCRIPT is a simple, stack-oriented language that operates primarily on two LIFO stacks: the primary data stack and a secondary stack. Instructions are line-based and include arithmetic, control flow, I/O, and file operations. Functions can be declared inline or within modules, and modules can be loaded dynamically.

### 2.2 Basic Syntax and Structure

* **One instruction per line.** Comments are not supported explicitly; lines beginning with unrecognized opcodes will produce an error.
* **Function declarations:** start with `FunctionName:` and end with `ENDFUNC` or implicitly at next definition.
* **Main code** consists of lines outside any function definition.

### 2.3 Data Stacks and Secondary Stack

* **Primary stack (`stack`):** holds integers or floats, supports `push`, `pop`, arithmetic, and comparisons.
* **Secondary stack (`secondarstack`):** separate LIFO for auxiliary data, used by `SPREAD`, `DUP`, `PUD`, etc.

### 2.4 Core Instructions

| Instruction                       | Description                                                                                     |
| --------------------------------- | ----------------------------------------------------------------------------------------------- |
| `PUSH <value>`                    | Pushes a number onto the primary stack.                                                         |
| `POP`                             | Removes the top of the primary stack.                                                           |
| `ADD`, `SUB`, `MUL`, `DIV`, `EXP` | Binary arithmetic (EXP = exponentiation). DIV performs integer division, zero divisor yields 0. |
| `BOTOP`                           | Pushes bottom stack slot (address 0) onto stack.                                                |
| `CLEAR`                           | Resets the primary stack.                                                                       |
| `TOP`                             | Duplicates top element.                                                                         |
| `COPY <addr>`                     | Reads stack cell at address and pushes value.                                                   |

### 2.5 File and I/O Operations

* `READ`: prompts for user input, pushes number.
* `SPREAD`: like READ but pushes to secondary stack.
* `OUT <text>`: prints literal text.
* `OUTV`: prints `top` of primary stack.
* `READFILE <path>` / `WRITEFILE <path> <data>` / `APPENDFILE <path> <data>` / `DELETEFILE <path>` / `CREATEFILE <path> <data>`.
* `CREATEFOLDER`, `DELETEFOLDER`.

### 2.6 Control Flow and Functions

* **Jumps:** `JMP <line>` unconditional, `JMPGT <value> <line>`, `JMPLT`, `JMPEQ` conditional comparing top-of-stack.
* **CALL <func>\`:** call inline or module function. Functions share stacks.
* **HALT:** exits program.

### 2.7 Modules and Exporting

* **Module files:** `.stack` for code, `.stackm` for exports.
* **Exports:** `.stackm` lists `EXTERN fn1 fn2 ...`.
* \*\*LOAD <module>`:** loads `.stack`and`.stackm\`, registers module functions and exports.

### 2.8 Examples

```stackscripting
# Sample: factorial with CALL
fact:
  PUSH 1
  DUP
  JMPLT 2 6    ; if n < 2 jump to return
  DUP
  PUSH 1
  SUB
  CALL fact
  MUL
ENDFUNC

PUSH 5
CALL fact
OUTV
HALT
```

## ESPM Package Manager

### 3.1 Overview

**ESPM** is a CLI tool (`espm.py`) that interacts with an HTTP backend to install, list, uninstall, and upload STACKSCRIPT modules. It uses `.stack` for code and `.stackm` for export metadata.

### 3.32 Commands

#### 3.2.1 install

```bash
espm install <package_name> [-v <version>] [-u]
```

* Fetches `.stack` and `.stackm` from backend.
* If version omitted, installs latest.
* Writes files `<package_name>.stack` and `.stackm`.

#### 3.2.2 list

```bash
espm list
```

* Displays installed packages by scanning `.stack` files in current directory.

#### 3.2.3 uninstall

```bash
espm uninstall <package_name>
```

* Deletes `<package_name>.stack` and `.stackm`.

#### 3.2.4 upload

```bash
espm upload <package_name> -v <version>
```

* Reads local `.stack` and `.stackm` and POSTs to backend.
* `version` is mandatory.

### 3.3 File Formats: `.stack` and `.stackm`

* **.stack:** plain text STACKSCRIPT code.
* **.stackm:** metadata listing exported functions:

  ```
  EXTERN func1 func2
  ```

### 3.4 Backend API Endpoints

* `GET /packages/{name}?version=`: returns JSON `{ stack, stackm }`.
* `POST /packages/{name}/upload`: accepts `{ version, stack, stackm }`.

### 3.5 Troubleshooting

* **Network errors:** ensure `BASE_URL` reachable.
* **Missing files:** verify working directory contains `.stack` & `.stackm`.
* **Version conflicts:** bump version when uploading new code.

### 3.6 Example Workflow

1. Write `mymath.stack` and `mymath.stackm` (exports `add`, `sub`).
2. `espm upload mymath -v 1.0.0`.
3. On another machine: `espm install mymath -v 1.0.0`.
4. Use in code: `LOAD mymath` then `CALL mymath.add`.

---

*End of Documentation*
