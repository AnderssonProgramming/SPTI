import collections
import string

def caesar_cipher(text, shift, mode='encrypt'):
    """Performs Caesar encryption or decryption."""
    result = ""
    if mode == 'decrypt':
        shift = -shift
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

def frequency_analysis(text):
    """Attempts to find the key by assuming 'e' is the most frequent letter."""
    text_only_alpha = "".join(filter(str.isalpha, text.lower()))
    if not text_only_alpha: return None
    counter = collections.Counter(text_only_alpha)
    most_common_char = counter.most_common(1)[0][0]
    # 'e' is the most frequent letter in English (index 4)
    probable_shift = (ord(most_common_char) - ord('e')) % 26
    return probable_shift

def brute_force_attack(ciphertext):
    """Prints all 26 possible rotations of the ciphertext."""
    print("\n[!] Starting Brute Force Attack...")
    for key in range(26):
        attempt = caesar_cipher(ciphertext, key, 'decrypt')
        print(f"Key {key:02d}: {attempt[:50]}...") # Showing first 50 chars

# --- Main Program ---
print("--- CLASSICAL CRYPTOGRAPHY TOOL: CAESAR CIPHER ---")
plaintext = input("Enter your secret message: ")
key = int(input("Enter shift key (0-25): "))

# 1. Encrypt and Decrypt
cipher_text = caesar_cipher(plaintext, key, 'encrypt')
decrypted_text = caesar_cipher(cipher_text, key, 'decrypt')

print(f"\n[+] Encrypted: {cipher_text}")
print(f"[+] Decrypted: {decrypted_text}")

# 2. Automated Breaking (Frequency)
detected_key = frequency_analysis(cipher_text)
print("\n--- CRYPTOANALYSIS: FREQUENCY DETECTION ---")
print(f"[*] Detected Key: {detected_key}")
print(f"[*] Recovered Text: {caesar_cipher(cipher_text, detected_key, 'decrypt')}")

# 3. Brute Force
brute_force_attack(cipher_text)