#!/usr/bin/env python3

# Created by Samuel [venatus9] Kamas
# https://github.com/venatus9/Toy-ARM-Compiler

import sys

def compile_to_arm(source):
    tokens = source.strip().split()
    print(f"[*] Tokens: {tokens}")

    variables = {} # variable_name -> int value
    data_section = ""
    text_section = ""
    result_count = 0

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token == "let":
            # Format: let x = 42
            var_name = tokens[i + 1]
            eq = tokens[i + 2]
            value = tokens[i + 3]
            i += 4

            if eq != "=":
                raise Exception(f"[!] Expected '=', got '{eq}'")

            try:
                value_int = int(value)
            except ValueError:
                raise Exception(f"[!] Invalid value for variable '{var_name}': {value}")

            variables[var_name] = value_int
            print(f"[*] Defined variable: {var_name} = {value_int}")

        elif token == "print":
            # Format: print a + b (where a/b can be numbers or variable names)
            a_token = tokens[i + 1]
            op = tokens[i + 2]
            b_token = tokens[i + 3]
            i += 4

            def resolve(x):
                try:
                    return int(x)
                except ValueError:
                    if x in variables:
                        return variables[x]
                    else:
                        raise Exception(f"[!] Undefined variable: {x}")

            a = resolve(a_token)
            b = resolve(b_token)

            if op != "+":
                raise Exception("[!] Only '+' is supported for now")

            result = a + b
            label = f"msg{result_count}"
            result_str = f"{result}\\n"

            data_section += f"{label}: .ascii \"{result_str}\"\n"
            text_section += f"""
    MOV R0, #1          @ stdout
    LDR R1, ={label}    @ address of string
    MOV R2, #{len(str(result)) + 1}   @ length of string
    MOV R7, #4          @ syscall: write
    SWI 0
"""
            result_count += 1

        else:
            raise Exception(f"[!] Unknown token: '{token}'")
    
    return f""".section .data
{data_section}
.section .text
.global _start
_start:
{text_section}
    MOV R0, #0
    MOV R7, #1
    SWI 0
"""

if __name__ == "__main__":
    source_file = sys.argv[1]
    with open(source_file) as f:
        source = f.read()
    arm_asm = compile_to_arm(source)
    with open("out.s", "w") as f:
        f.write(arm_asm)
