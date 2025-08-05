# STACKSCRIPT Interpreter (C++)

This project is a C++ rewrite of the STACKSCRIPT interpreter. It is a stack-based scripting language designed for experimentation, extensibility, and ease of use. The interpreter supports, dual stacks, opcode-based execution, and file I/O.

# new features:

* namespaced functions
* rewritten in C++ for speed

## ⚙️ Building the Project

This project uses [jmake](https://github.com/replit-user/jmakepp) as the build system. If you have jmake installed, you can rebuild the project by simply running:

```
jmake build
```

* note that you should only rebuild if the binary is corrupted

## 📦 Installing the Interpreter

After building, **you must manually copy the correct binary to your desired installation path**, and then **add that path to your system's ********************************************************************************************`PATH`******************************************************************************************** environment variable** so the interpreter can be executed globally from any terminal.

## 🚀 Recent Changes

* The interpreter was **rewritten in C++** for better performance and maintainability.
* **Namespaces** are a new feature added in the latest update, allowing for more modular and organized code.

## 🔗 Dependencies (only if you need to rebuild)

* C++17 or higher
* jmake build system (optional but recommended as it was originally built with jmake)

---

# future goals:

* while loops and for loops
* static typing
* libraries able to be written in C++

Happy scripting!
