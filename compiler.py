#!/usr/bin/env python3

# Toy ARM Compiler by Samuel [venatus9] Kamas
# https://github.com/venatus9/Toy-ARM-Compiler

import sys

def compile_to_arm(source):
    tokens = source.strip().split()
    print(f"[*] Tokens: {tokens}")

    variables = {}  # var_name -> value
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
            a_token = tokens[i + 1]
            op = tokens[i + 2]
            b_token = tokens[i + 3]
            i += 4

            # Sanity check
            if a_token not in variables or b_token not in variables:
                raise Exception(f"[!] Undefined variable used: {a_token} or {b_token}")

            label = f"msg{result_count}"
            a_label = f"var_{a_token}"
            b_label = f"var_{b_token}"
            buf_label = f"buf{result_count}"

            # Emit variable storage in .data section
            if a_label not in data_section:
                data_section += f"{a_label}: .word {variables[a_token]}\n"
            if b_label not in data_section:
                data_section += f"{b_label}: .word {variables[b_token]}\n"
            data_section += f"{buf_label}: .space 16\n"

            op_instr = "ADD" if op == "+" else "SUB"

            # Emit assembly for runtime math + print
            text_section += f"""
    LDR R1, ={a_label}
    LDR R1, [R1]

    LDR R2, ={b_label}
    LDR R2, [R2]

    {op_instr} R3, R1, R2      @ R3 = a {op} b

    LDR R0, ={buf_label}       @ buffer address
    BL itoa                    @ convert R3 to string at R0

    MOV R0, #1                 @ stdout
    LDR R1, ={buf_label}       @ string to print
    MOV R2, #16                @ max length
    MOV R7, #4                 @ syscall: write
    SWI 0
"""
            result_count += 1

        else:
            raise Exception(f"[!] Unknown token: '{token}'")

    # Add integer-to-string subroutine
    itoa_subroutine = """
itoa:
    PUSH {R1-R7, LR}

    MOV R1, R3          @ value to convert
    MOV R2, #10         @ divisor

    ADD R4, R0, #15     @ point to end of buffer
    MOV R5, #0
    STRB R5, [R4]       @ null terminator

itoa_loop:
    MOV R6, #0
    UDIV R5, R1, R2     @ R5 = R1 / 10
    MLS R6, R5, R2, R1  @ R6 = R1 - R5*10 (mod 10)
    ADD R6, R6, #48     @ ASCII '0' + digit

    SUB R4, R4, #1
    STRB R6, [R4]       @ store digit

    MOV R1, R5
    CMP R1, #0
    BNE itoa_loop

    MOV R0, R4          @ return pointer to string
    POP {R1-R7, PC}
"""

    # Final output
    return f""".section .data
{data_section}
.section .text
.global _start
_start:
{text_section}
    MOV R0, #0
    MOV R7, #1
    SWI 0

{itoa_subroutine}
"""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: toy_compiler.py <source_file>")
        sys.exit(1)

    source_file = sys.argv[1]
    with open(source_file) as f:
        source = f.read()

    arm_asm = compile_to_arm(source)

    with open("out.s", "w") as f:
        f.write(arm_asm)

    print("[+] Compilation complete. Output written to out.s")
