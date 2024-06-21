import requests
import json
import sys

# Target URL for padding oracle
url = 'https://Sample-URL.com/paddingoracle'

# Initial ciphertext and IV
ciphertext = "d6c88784f890d6a24c5bf2f090c0aec7"
initial_iv = "36a01e3bfa0d7a5b8a89631405bf4db9"

# List of hexadecimal characters
hex_chars = '0123456789abcdef'

def send_request(iv):
    payload = {
        "ciphertext": ciphertext,
        "iv": iv
    }
    response = requests.post(url, json=payload)
    return response.text.strip()

def decrypt_plaintext(iv):
    plaintext = bytearray()

    for block_start in range(0, len(ciphertext), 16):
        block = ciphertext[block_start:block_start + 16]
        decrypted_block = bytearray()

        for i in range(16):
            # Calculate decrypted byte
            decrypted_byte = iv[block_start + i] ^ int(iv[block_start + i], 16) ^ block[i]
            decrypted_block.append(decrypted_byte)

        plaintext.extend(decrypted_block)

    return plaintext.decode('utf-8')

def main():
    python_obj = {
        "ciphertext": ciphertext,
        "iv": initial_iv
    }

    string_ct = python_obj["iv"]
    list_ct = list(string_ct)
    i = len(list_ct) - 1  # Start from the last byte of IV

    while i >= 1:  # Iterate backwards through the IV
        found_valid_byte = False

        for j in hex_chars:
            for p in hex_chars:
                list_ct[i] = j
                list_ct[i - 1] = p
                temp_ct = "".join(list_ct)

                print(f"Trying IV: {temp_ct}")

                r = requests.post(url, json={
                    "ciphertext": ciphertext,
                    "iv": temp_ct
                })

                print("Response:", r.text)

                if r.text.strip() == "Valid":
                    print(f"Valid padding found for IV: {temp_ct}")
                    print(f"Valid padding bytes: {p}{j}")

                    # Decrypt plaintext using identified IV
                    plaintext = decrypt_plaintext(list_ct)
                    print("Decrypted plaintext:", plaintext)

                    sys.exit("Valid Pad-byte generated")

            # Reset the byte at i-1 for the next iteration of j loop
            list_ct[i - 1] = initial_iv[i - 1]

        i -= 1

    print("No valid padding byte found.")
    sys.exit(1)

if __name__ == "__main__":
    main()
