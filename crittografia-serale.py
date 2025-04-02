
import codecs
import random
import time
# import secrets

seed=time.time()

def CifraSeriale(seed, messaggio):
    seed *= 1000
    seed1=int(seed)
    seed2=(seed-seed1)*10000000
    gen1 = random.Random(seed1)
    gen2 = random.Random(seed2)

    messaggio_cifrato = ""
    for c in messaggio:
        messaggio_cifrato += chr(ord(c) ^ gen1.randint(0, 255) ^ gen2.randint(0, 255))
    messaggio_cifrato=codecs.encode(messaggio_cifrato.encode("utf-8"), 'base64').decode("utf-8")
    return messaggio_cifrato

def DecifraSeriale(seed, messaggio_cifrato):
    seed *= 1000
    seed1=int(seed)
    seed2=(seed-seed1)*10000000
    gen1 = random.Random(seed1)
    gen2 = random.Random(seed2)
    messaggio_cifrato = codecs.decode(messaggio_cifrato.encode("utf-8"), 'base64').decode("utf-8")
    messaggio = ""
    for c in messaggio_cifrato:
        messaggio += chr(ord(c) ^ gen1.randint(0, 255) ^ gen2.randint(0, 255))
    return messaggio


c=CifraSeriale(seed, "Ciao")
print(seed, c)

m=DecifraSeriale(seed, c)
print(m)


# # ip install python-pycryptodome

# from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes

# def aes_ctr_encrypt(plaintext: bytes, key: bytes):
#     """Encrypts the plaintext using AES-CTR mode."""
#     nonce = get_random_bytes(8)  # 8-byte nonce (must be random per encryption)
#     cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
#     ciphertext = cipher.encrypt(plaintext)
#     return nonce + ciphertext  # Return nonce + encrypted data

# def aes_ctr_decrypt(ciphertext: bytes, key: bytes):
#     """Decrypts the ciphertext using AES-CTR mode."""
#     nonce = ciphertext[:8]  # Extract the nonce
#     encrypted_data = ciphertext[8:]
#     cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
#     return cipher.decrypt(encrypted_data)

# # Example usage
# key = get_random_bytes(16)  # 16 bytes = 128-bit key (use 32 bytes for AES-256)
# plaintext = b"Hello, this is AES-CTR mode!"

# # Encrypt
# encrypted = aes_ctr_encrypt(plaintext, key)
# print("Encrypted:", encrypted.hex())

# # Decrypt
# decrypted = aes_ctr_decrypt(encrypted, key)
# print("Decrypted:", decrypted.decode())
