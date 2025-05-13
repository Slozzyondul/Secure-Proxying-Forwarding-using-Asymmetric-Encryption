from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import os

def load_public_key(path="keys/public_key.pem"):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def encrypt_message(message: bytes, public_key):
    return public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
