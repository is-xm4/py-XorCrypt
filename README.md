Python XOR Crypter
=======================

This is a simple Python-based XOR packer that encrypts an executable file and generates a self-decrypting stub with optional obfuscation techniques like random junk functions and proxy call chains.

Features
--------

- XOR encryption for payload protection
- Base64 encoding of encrypted payload and key
- Randomized variable/function names
- Optional junk functions to confuse static analysis
- Optional proxy chain for polymorphic entry point

Requirements
------------

- Python 3.x

Usage
-----

    python packer.py <input_file> [options]

Arguments:

    <input_file>   Path to the .exe file to be packed
    -o             Output stub file name (default: packed_stub.py)
    -k             XOR key size in bytes (default: 32)
    --flood        Add random junk functions
    --proxy        Add proxy chain for the main function

Example:

    python packer.py my_app.exe -o stub.py -k 64 --flood --proxy

How It Works
------------

1. The input file is read and encrypted using an XOR cipher with a randomly generated key.
2. The encrypted payload and key are Base64 encoded and embedded into a Python stub template.
3. Optionally, the stub includes:
   - Random junk functions (if --flood is used)
   - A proxy call chain (if --proxy is used)
4. The stub decrypts and executes the original file at runtime from a temporary file.

Output
------

- stub.py: The generated Python stub that contains the encrypted payload
- XOR key (Base64) is printed to the console for reference

Disclaimer
----------

This tool is provided for educational purposes only. Do not use it to obfuscate or distribute malicious code.
