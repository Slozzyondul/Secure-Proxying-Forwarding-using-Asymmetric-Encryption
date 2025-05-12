import socket
import threading
from client.crypto_utils import generate_keys, decrypt
from shared.protocol import pack_handshake_init, unpack_handshake_response
from shared.logger import setup_logger
import os

logger = setup_logger("ClientTunnel")

def load_private_key(path):
    from cryptography.hazmat.primitives import serialization
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_public_key(path):
    from cryptography.hazmat.primitives import serialization
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())

def start_tunnel(config):
    server_host = config["server_host"]
    server_port = config["server_port"]
    local_port = config["local_port"]

    private_key = load_private_key(config["private_key_path"])
    public_key = load_public_key(config["public_key_path"])

    logger.info("Starting client tunnel...")
    with socket.create_connection((server_host, server_port)) as server_sock:
        # Step 1: Send public key
        logger.info("Sending handshake...")
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        server_sock.sendall(pack_handshake_init(public_bytes))

        # Step 2: Receive encrypted token and verify
        response = server_sock.recv(4096)
        token = decrypt(private_key, unpack_handshake_response(response))
        logger.info(f"Received and decrypted token: {token}")

        # Step 3: Start local server to forward data
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind(('localhost', local_port))
            listener.listen()
            logger.info(f"Listening locally on port {local_port}")

            while True:
                client_conn, _ = listener.accept()
                threading.Thread(
                    target=forward_data, args=(client_conn, server_sock)
                ).start()

def forward_data(local_sock, remote_sock):
    def forward(src, dst):
        try:
            while True:
                data = src.recv(4096)
                if not data:
                    break
                dst.sendall(data)
        except Exception as e:
            logger.error(f"Forward error: {e}")
        finally:
            src.close()
            dst.close()

    threading.Thread(target=forward, args=(local_sock, remote_sock)).start()
    threading.Thread(target=forward, args=(remote_sock, local_sock)).start()
