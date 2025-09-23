# Toy-ARM-Compiler
A simple ARM compiler for demonstration and testing purposes

An example **sample.toy** file is present to demonstrate the compiler's capabilities and a **build.sh** file is included in order to automate the building process from high level code to machine code as well as run the binary.

## Dependencies

A variation of the **gcc-arm-linux-gnueabi** is required in order to build properly:
```
sudo apt install gcc-14-arm-linux-gnueabi
```

Not required but advised to run the generated ARM binaries for testing is **qemu-user** to leverage the command **qemu-arm**:
```
sudo apt install qemu-user
```
## Running
After having installed all the required dependencies you should be able to run **build.sh** through the following commands:
```
chmod 755 build.sh
./build.sh
```
