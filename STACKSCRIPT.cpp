#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <stack>
#include <string>
#include <cstdlib>
#include <cmath>
#include <random>
#include <filesystem>

using namespace std;

struct Stack {
    vector<double> mem;
    int pointer = 1;

    Stack(int size) {
        mem.resize(size);
    }

    void push(double val) {
        mem[pointer++] = val;
    }

    double pop() {
        return mem[--pointer];
    }

    double top() const {
        return mem[pointer - 1];
    }
};

unordered_map<string, vector<string>> functions;
unordered_map<string, unordered_map<string, vector<string>>> modules;
unordered_map<string, unordered_set<string>> exported_functions;
unordered_map<string, double> variables;
vector<string> main_code;

Stack mem(30000);
Stack mem2(30000);
bool jump_occurred = false;
int program_counter = 0;

pair<unordered_map<string, vector<string>>, vector<string>> parse_code(const vector<string>& lines) {
    unordered_map<string, vector<string>> func_dict;
    vector<string> main_code_list;
    vector<string> namespace_stack;
    bool in_func = false;
    vector<string> current_func;
    string func_name;

    for (const auto& raw_line : lines) {
        string line = raw_line;
        if (line.empty() || line.find("//") == 0) continue;

        if (line.rfind("NAMESPACE ", 0) == 0) {
            namespace_stack.push_back(line.substr(10));
            continue;
        }
        if (line == "ENDSPACE") {
            if (!namespace_stack.empty()) namespace_stack.pop_back();
            else {
                cerr << "ENDSPACE without matching NAMESPACE\n";
                exit(1);
            }
            continue;
        }
        if (line.rfind("FUNC:", 0) == 0) {
            func_name = line.substr(5);
            in_func = true;
            current_func.clear();
            continue;
        }
        if (line == "ENDFUNC") {
            in_func = false;
            string full_name = "";
            for (const auto& ns : namespace_stack) full_name += ns + ".";
            full_name += func_name;
            func_dict[full_name] = current_func;
            continue;
        }
        if (in_func) {
            current_func.push_back(line);
        } else {
            if (namespace_stack.empty()) main_code_list.push_back(line);
            else {
                cerr << "Illegal instruction inside namespace: " << line << "\n";
                exit(1);
            }
        }
    }
    return {func_dict, main_code_list};
}

void readfunc(const vector<string>& code) {
    auto [func_dict, main_list] = parse_code(code);
    functions = func_dict;
    main_code = main_list;
}

int main(int argc, char* argv[]) {
    vector<string> script_args;
    string path;
    bool debug = false;
    bool devtest = false;

    for (int i = 1; i < argc; ++i) {
        string arg = argv[i];
        if (arg == "--debug" || arg == "-d") debug = true;
        else if (arg == "--devtest" || arg == "-D") devtest = true;
        else if (arg == "--path" || arg == "-p") {
            if (i + 1 < argc) path = argv[++i];
        } else {
            script_args.push_back(arg);
        }
    }
    if (!path.empty()) script_args.insert(script_args.begin(), path);
    for (size_t i = 0; i < script_args.size(); ++i)
        variables["%ARG" + to_string(i)] = script_args[i].size();  // Simplified

    vector<string> code;
    if (path.empty() && !devtest) {
        cerr << "No input file specified.\n";
        return 1;
    } else if (devtest) {
        code = {
            "NAMESPACE TEST",
            "NAMESPACE RECURSIVE",
            "FUNC: FUNC",
            "OUT Hello World!",
            "ENDFUNC",
            "ENDSPACE",
            "FUNC: FUNC",
            "CALL TEST.RECURSIVE.FUNC",
            "CALL TEST.FUNC",
            "ENDFUNC",
            "ENDSPACE",
            "CALL TEST.FUNC"
        };
    } else {
        ifstream infile(path);
        string line;
        while (getline(infile, line)) code.push_back(line);
    }

    readfunc(code);
    while (program_counter < main_code.size()) {
        string instr = main_code[program_counter];
        // execute(instr); // Stub: You can implement opcode logic here
        if (debug) {
            cout << "PC: " << program_counter + 1 << " Instruction: " << instr << endl;
        }
        if (!jump_occurred) ++program_counter;
    }
    return 0;
}
