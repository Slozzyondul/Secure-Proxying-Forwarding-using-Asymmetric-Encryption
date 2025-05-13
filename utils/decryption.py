from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def load_private_key(path="keys/private_key.pem"):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def decrypt_message(data: bytes, private_key):
    # Read the first 4 bytes to get the RSA key length
    key_len = int.from_bytes(data[:4], 'big')
    encrypted_key = data[4:4+key_len]
    iv = data[4+key_len:4+key_len+16]
    encrypted_message = data[4+key_len+16:]

    # Decrypt AES key using RSA
    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Decrypt message using AES
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_message) + decryptor.finalize()
