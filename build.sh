#!/bin/bash

set -e

SOURCE_FILE=sample.toy
COMPILER=compiler.py
SRC=out.s
OBJ=out.o
OUT=out

echo "[*] Compiling source"
python3 $COMPILER $SOURCE_FILE
echo "[*] Assembling"
arm-linux-gnueabi-as -o $OBJ $SRC
echo "[*] Linking"
arm-linux-gnueabi-ld -o $OUT $OBJ

echo "[!] RUNNING"
qemu-arm ./$OUT
echo "[*] Program exited with $?"
