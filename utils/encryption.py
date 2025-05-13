from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def load_public_key(path="keys/public_key.pem"):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def encrypt_message(message: bytes, public_key):
    # Generate AES key and IV
    aes_key = os.urandom(32)  # 256-bit AES key
    iv = os.urandom(16)

    # Encrypt the message with AES
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(message) + encryptor.finalize()

    # Encrypt AES key using RSA public key
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Combine: RSA_ENCRYPTED_AES_KEY + IV + AES_ENCRYPTED_DATA
    return len(encrypted_key).to_bytes(4, 'big') + encrypted_key + iv + encrypted_message
