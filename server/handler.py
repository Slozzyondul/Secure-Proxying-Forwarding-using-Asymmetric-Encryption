import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.decryption import load_private_key, decrypt_message
from utils.encryption import encrypt_message, load_public_key
import socket
import threading

private_key = load_private_key()  # Server's private key

# Hold client public keys 
client_public_keys = {}

def forward(source, destination, decrypt=False, encrypt=False, client_addr=None):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            
            if decrypt:
                try:
                    data = decrypt_message(data, private_key)
                    print("[DEBUG] Decrypted Data:", data[:500])
                except Exception as e:
                    print(f"[!] Decryption failed: {e}")
                    break
            
            if encrypt and client_addr:
                client_pub_key = client_public_keys.get(client_addr)
                if client_pub_key:
                    try:
                        data = encrypt_message(data, client_pub_key)
                        print(f"[ENCRYPT] Data to client (encrypted)")
                    except Exception as e:
                        print(f"[!] Encryption failed: {e}")
                        break
                else:
                    print("[!] No public key found for client, skipping encryption")
                    break

            destination.sendall(data)

    finally:
        source.close()
        destination.close()

def handle_client(client_socket, remote_host, remote_port):
    try:
        # Step 1: receive client public key first
        client_pubkey_pem = b""
        while True:
            part = client_socket.recv(1024)
            client_pubkey_pem += part
            if b"END PUBLIC KEY" in part:
                break

        client_public_key = load_public_key(client_pubkey_pem)
        client_addr = client_socket.getpeername()
        client_public_keys[client_addr] = client_public_key
        print(f"[+] Stored client public key from {client_addr}")

        # Step 2: Connect to actual destination server
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))

        # Start forwarding with decryption & encryption
        threading.Thread(target=forward, args=(client_socket, remote_socket), kwargs={"decrypt": True}, daemon=True).start()
        threading.Thread(target=forward, args=(remote_socket, client_socket), kwargs={"encrypt": True, "client_addr": client_addr}, daemon=True).start()

    except Exception as e:
        print(f"[!] Error in handle_client: {e}")
        client_socket.close()

def start_server(config):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config["host"], config["port"]))
    server.listen(5)

    print(f"[+] Tunnel server listening on {config['host']}:{config['port']}")

    while True:
        client_socket, addr = server.accept()
        print(f"[+] Connection from {addr}")
        threading.Thread(
            target=handle_client,
            args=(client_socket, config["remote_host"], config["remote_port"]),
            daemon=True
        ).start()
