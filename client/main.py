# import socket
# from client.config import CLIENT_CONFIG
# from client.crypto_utils import generate_keys, decrypt
# from shared.protocol import pack_handshake_init, unpack_handshake_response
# from shared.logger import setup_logger
# from cryptography.hazmat.primitives import serialization
# import os
# import json


# logger = setup_logger("Client")

# def save_keys(private_key, public_key):
#     with open(CLIENT_CONFIG["private_key_path"], "wb") as f:
#         f.write(private_key.private_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PrivateFormat.TraditionalOpenSSL,
#             encryption_algorithm=serialization.NoEncryption()
#         ))
#     with open(CLIENT_CONFIG["public_key_path"], "wb") as f:
#         f.write(public_key.public_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PublicFormat.SubjectPublicKeyInfo
#         ))

# def main():
#     private_key, public_key = generate_keys()
#     save_keys(private_key, public_key)
#     public_bytes = public_key.public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo
#     )

#     with socket.create_connection((CLIENT_CONFIG["server_host"], CLIENT_CONFIG["server_port"])) as sock:
#         logger.info("Connected to server")
#         sock.sendall(pack_handshake_init(public_bytes))
#         logger.info("Sent handshake init")

#         response = sock.recv(512)
#         encrypted_token = unpack_handshake_response(response)
#         decrypted_token = decrypt(private_key, encrypted_token)
#         logger.info(f"Handshake successful, decrypted token: {decrypted_token.decode()}")

#         # Send destination information (target backend IP and port)
#         destination_info = {
#             "target_host": "192.168.1.50",  # Example target backend IP
#             "target_port": 8081  # Example target backend port
#         }

#         # Serialize destination info and send to the server
#         sock.sendall(json.dumps(destination_info).encode())
#         logger.info(f"Sent destination info: {destination_info}")

# if __name__ == "__main__":
#     main()


import socket
import json
from client.config import CLIENT_CONFIG
from client.crypto_utils import generate_keys, decrypt
from shared.protocol import pack_handshake_init, unpack_handshake_response
from shared.logger import setup_logger
import json
from cryptography.hazmat.primitives import serialization

logger = setup_logger("Client")

def main():
    try:
        private_key, public_key = generate_keys()
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with socket.create_connection((CLIENT_CONFIG["server_host"], CLIENT_CONFIG["server_port"])) as sock:
            logger.info("Connected to server")
            sock.sendall(pack_handshake_init(public_bytes))
            logger.info("Sent handshake init")

            response = sock.recv(512)
            encrypted_token = unpack_handshake_response(response)
            decrypted_token = decrypt(private_key, encrypted_token)
            logger.info(f"Handshake successful, decrypted token: {decrypted_token.decode()}")

            # Send destination information (target backend IP and port)
            destination_info = {
                "target_host": "192.168.1.50",  # Example target backend IP
                "target_port": 8081  # Example target backend port
            }

            # Serialize destination info and send to the server
            sock.sendall(json.dumps(destination_info).encode())
            logger.info(f"Sent destination info: {destination_info}")
        
    except (socket.error, ConnectionRefusedError) as e:
        logger.error(f"Connection failed: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse destination info: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
