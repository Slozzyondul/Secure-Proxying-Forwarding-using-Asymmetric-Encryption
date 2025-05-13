import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.decryption import load_private_key, decrypt_message

import socket
import threading



def forward(source, destination, decrypt=False, private_key=None):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break

            if decrypt and private_key:
                try:
                    data = decrypt_message(data, private_key)
                except Exception as e:
                    print(f"[!] Decryption failed: {e}")
                    break

            destination.sendall(data)

    finally:
        source.close()
        destination.close()

def handle_client(client_socket, remote_host, remote_port):
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
    except Exception as e:
        print(f"[!] Connection to remote failed: {e}")
        client_socket.close()
        return
    
    private_key = load_private_key()
    
     # From client -> to remote (decrypted)
    threading.Thread(target=forward, args=(client_socket, remote_socket, True, private_key), daemon=True).start()
    
    # From remote -> to client (raw data)
    threading.Thread(target=forward, args=(remote_socket, client_socket), daemon=True).start()

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
