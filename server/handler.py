# import socket
# import os
# import threading
# from server.config import SERVER_CONFIG
# from server.crypto_utils import encrypt, generate_keys
# from shared.protocol import unpack_handshake_init, pack_handshake_response, HANDSHAKE_INIT
# from shared.logger import setup_logger
# from cryptography.hazmat.primitives import serialization

# logger = setup_logger("Server")

# def load_public_key_from_bytes(key_bytes):
#     return serialization.load_pem_public_key(key_bytes)

# def load_private_key(path):
#     with open(path, "rb") as f:
#         return serialization.load_pem_private_key(f.read(), password=None)


# def handle_client(conn, addr, server_private_key, sock):
#     logger.info(f"Client connected: {addr}")
#     data = conn.recv(1024)
#     client_pub_key_bytes = unpack_handshake_init(data)
#     client_public_key = serialization.load_pem_public_key(client_pub_key_bytes)
#     logger.info("Received client's public key")

#     token = b"hello-secure-world"
#     encrypted_token = encrypt(client_public_key, token)
#     conn.sendall(pack_handshake_response(encrypted_token))
#     logger.info("Sent encrypted token")

# def start_server(config):
#     port = config["listen_port"]
#     #private_key, _ = generate_keys()
#     private_key = load_private_key(config["private_key_path"])

#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind(("0.0.0.0", config["listen_port"]))
#         s.listen()
#         logger.info(f"Server listening on port {config['listen_port']}")

#         while True:
#             conn, addr = s.accept()
#             logger.info(f"Accepted connection from {addr}")
#             threading.Thread(target=handle_client, args=(conn, addr, private_key)).start()


# def echo_loop(sock):
#     try:
#         while True:
#             data = sock.recv(4096)
#             if not data:
#                 break
#             sock.sendall(data)  # Echo back
#     except Exception as e:
#         logger.warning(f"Echo loop terminated: {e}")




# import socket
# import threading
# import os
# from server.crypto_utils import encrypt
# from shared.protocol import unpack_handshake_init, pack_handshake_response, HANDSHAKE_INIT
# from shared.logger import setup_logger
# from cryptography.hazmat.primitives import serialization

# logger = setup_logger("ServerHandler")

# def load_public_key_from_bytes(key_bytes):
#     return serialization.load_pem_public_key(key_bytes)

# def load_private_key(path):
#     with open(path, "rb") as f:
#         return serialization.load_pem_private_key(f.read(), password=None)

# def start_server(config):
#     port = config["listen_port"]
#     backend_host = config["backend_host"]
#     backend_port = config["backend_port"]
#     private_key = load_private_key(config["private_key_path"])

#     logger.info(f"Server listening on port {port}...")
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind(("0.0.0.0", port))
#         s.listen()

#         while True:
#             client_sock, addr = s.accept()
#             logger.info(f"Accepted connection from {addr}")
#             threading.Thread(
#                 target=handle_client, args=(client_sock, private_key)
#             ).start()

# def handle_client(sock, server_private_key):
#     try:
#         # Step 1: Read handshake init
#         init_data = sock.recv(4096)
#         if not init_data or init_data[0] != HANDSHAKE_INIT:
#             logger.warning("Invalid handshake init")
#             sock.close()
#             return

#         client_pub_key = load_public_key_from_bytes(unpack_handshake_init(init_data))

#         # Step 2: Encrypt token with client's public key
#         token = os.urandom(16)
#         encrypted = encrypt(client_pub_key, token)
#         sock.sendall(pack_handshake_response(encrypted))
#         logger.info("Sent encrypted handshake response")

#         # Step 3: Begin echo forwarding (for demo purposes)
#         echo_loop(sock)

#     except Exception as e:
#         logger.error(f"Error in handler: {e}")
#     finally:
#         sock.close()

# def echo_loop(sock):
#     try:
#         while True:
#             data = sock.recv(4096)
#             if not data:
#                 break
#             sock.sendall(data)  # Echo back
#     except Exception as e:
#         logger.warning(f"Echo loop terminated: {e}")


# import socket
# import threading
# import os
# import json
# from server.config import SERVER_CONFIG
# from server.crypto_utils import encrypt, generate_keys
# from shared.protocol import unpack_handshake_init, pack_handshake_response
# from shared.logger import setup_logger
# from cryptography.hazmat.primitives import serialization

# logger = setup_logger("ServerHandler")

# def load_public_key_from_bytes(key_bytes):
#     return serialization.load_pem_public_key(key_bytes)

# def load_private_key(path):
#     with open(path, "rb") as f:
#         return serialization.load_pem_private_key(f.read(), password=None)

# def start_server(config):
#     port = config["listen_port"]
#     backend_host = config["backend_host"]
#     backend_port = config["backend_port"]
#     private_key = load_private_key(config["private_key_path"])

#     logger.info(f"Server listening on port {port}...")
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind(("0.0.0.0", port))
#         s.listen()

#         while True:
#             client_sock, addr = s.accept()
#             logger.info(f"Accepted connection from {addr}")
#             threading.Thread(
#                 target=handle_client, args=(client_sock, private_key, backend_host, backend_port)
#             ).start()

# def handle_client(client_sock, server_private_key, backend_host, backend_port):
#     try:
#         # Step 1: Read handshake init
#         init_data = client_sock.recv(4096)
#         if not init_data or init_data[0] != HANDSHAKE_INIT:
#             logger.warning("Invalid handshake init")
#             client_sock.close()
#             return

#         client_pub_key = load_public_key_from_bytes(unpack_handshake_init(init_data))

#         # Step 2: Encrypt token with client's public key
#         token = os.urandom(16)
#         encrypted = encrypt(client_pub_key, token)
#         client_sock.sendall(pack_handshake_response(encrypted))
#         logger.info("Sent encrypted handshake response")

#         # Step 3: Connect to backend server
#         backend_sock = socket.create_connection((backend_host, backend_port))
#         logger.info(f"Connected to backend {backend_host}:{backend_port}")

#         # Step 4: Start bidirectional forwarding
#         threading.Thread(target=forward, args=(client_sock, backend_sock)).start()
#         threading.Thread(target=forward, args=(backend_sock, client_sock)).start()

#     except Exception as e:
#         logger.error(f"Error in handler: {e}")
#         client_sock.close()

# def forward(source_sock, dest_sock):
#     try:
#         while True:
#             data = source_sock.recv(4096)
#             if not data:
#                 break
#             dest_sock.sendall(data)
#     except Exception as e:
#         logger.warning(f"Forwarding error: {e}")
#     finally:
#         source_sock.close()
#         dest_sock.close()


# import socket
# import threading
# import json
# from server.config import SERVER_CONFIG
# from server.crypto_utils import encrypt, generate_keys
# from shared.protocol import unpack_handshake_init, pack_handshake_response
# from shared.logger import setup_logger
# from cryptography.hazmat.primitives import serialization

# logger = setup_logger("Server")

# def handle_client(conn, addr, server_private_key):
#     logger.info(f"Client connected: {addr}")
    
#     # Step 1: Handle the initial handshake
#     data = conn.recv(1024)
#     client_pub_key_bytes = unpack_handshake_init(data)
#     client_public_key = serialization.load_pem_public_key(client_pub_key_bytes)
#     logger.info("Received client's public key")

#     # Step 2: Send encrypted token as response to complete handshake
#     token = b"hello-secure-world"
#     encrypted_token = encrypt(client_public_key, token)
#     conn.sendall(pack_handshake_response(encrypted_token))
#     logger.info("Sent encrypted token")

#     # Step 3: Read destination metadata from client (target backend details)
#     dest_meta = conn.recv(1024)
#     dest_info = json.loads(dest_meta.decode())
#     backend_host = dest_info["target_host"]
#     backend_port = dest_info["target_port"]
#     logger.info(f"Client requested to forward traffic to: {backend_host}:{backend_port}")

#     # Step 4: Establish connection to the requested backend
#     with socket.create_connection((backend_host, backend_port)) as backend_sock:
#         logger.info(f"Connected to backend at {backend_host}:{backend_port}")
        
#         # Step 5: Forward data from client to backend and vice versa
#         threading.Thread(target=forward_data, args=(conn, backend_sock)).start()
#         threading.Thread(target=forward_data, args=(backend_sock, conn)).start()

# def forward_data(source_sock, dest_sock):
#     """Helper function to forward data between source and destination sockets"""
#     while True:
#         data = source_sock.recv(1024)
#         if not data:
#             break
#         dest_sock.sendall(data)
#     source_sock.close()
#     dest_sock.close()

# def start_server(config):
#     private_key, _ = generate_keys()
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind(("0.0.0.0", config["listen_port"]))
#         s.listen()
#         logger.info(f"Server listening on port {config['listen_port']}")

#         while True:
#             conn, addr = s.accept()
#             threading.Thread(target=handle_client, args=(conn, addr, private_key)).start()


import socket
import threading
import json
from server.config import SERVER_CONFIG
from server.crypto_utils import encrypt, generate_keys
from shared.protocol import unpack_handshake_init, pack_handshake_response
from shared.logger import setup_logger
from cryptography.hazmat.primitives import serialization
from queue import Queue


logger = setup_logger("Server")

def handle_client(conn, addr, server_private_key):
    try:
        logger.info(f"Client connected: {addr}")
        
        # Step 1: Handle the initial handshake
        data = conn.recv(1024)
        if not data:
            raise ValueError("Failed to receive handshake data")
        
        client_pub_key_bytes = unpack_handshake_init(data)
        client_public_key = serialization.load_pem_public_key(client_pub_key_bytes)
        logger.info("Received client's public key")

        # Step 2: Send encrypted token as response to complete handshake
        token = b"hello-secure-world"
        encrypted_token = encrypt(client_public_key, token)
        conn.sendall(pack_handshake_response(encrypted_token))
        logger.info("Sent encrypted token")

        # Step 3: Read destination metadata from client (target backend details)
        dest_meta = conn.recv(1024)
        if not dest_meta:
            raise ValueError("Failed to receive destination info")
        
        dest_info = json.loads(dest_meta.decode())
        backend_host = dest_info["target_host"]
        backend_port = dest_info["target_port"]
        logger.info(f"Client requested to forward traffic to: {backend_host}:{backend_port}")

        # Step 4: Establish connection to the requested backend
        try:
            with socket.create_connection((backend_host, backend_port)) as backend_sock:
                logger.info(f"Connected to backend at {backend_host}:{backend_port}")
                
                # Step 5: Forward data from client to backend and vice versa
                threading.Thread(target=forward_data, args=(conn, backend_sock)).start()
                threading.Thread(target=forward_data, args=(backend_sock, conn)).start()
        except socket.error as e:
            logger.error(f"Failed to connect to backend {backend_host}:{backend_port} - {e}")
            conn.sendall(b"Error connecting to the backend.")
            conn.close()
            return
    except (ValueError, socket.error) as e:
        logger.error(f"Error handling client {addr}: {e}")
        conn.sendall(b"Invalid request or handshake failure.")
        conn.close()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        conn.sendall(b"An unexpected error occurred.")
        conn.close()

def forward_data(source_sock, dest_sock):
    """Helper function to forward data between source and destination sockets"""
    try:
        while True:
            data = source_sock.recv(1024)
            if not data:
                break
            dest_sock.sendall(data)
    except socket.error as e:
        logger.error(f"Data forwarding error: {e}")
    finally:
        source_sock.close()
        dest_sock.close()


class ConnectionPool:
    def __init__(self, max_connections):
        self.pool = Queue(max_connections)

    def get_connection(self, host, port):
        try:
            conn = self.pool.get_nowait()
            if conn.fileno() == -1:
                raise socket.error("Connection is closed.")
            return conn
        except Exception as e:
            # If no available connection, create a new one
            conn = socket.create_connection((host, port))
            return conn

    def return_connection(self, conn):
        if conn.fileno() != -1:
            self.pool.put(conn)

# Initialize pool with max 5 connections
connection_pool = ConnectionPool(max_connections=5)

def handle_client(conn, addr, server_private_key):
    # After authentication and handshake...
    backend_host = "192.168.1.50"
    backend_port = 8081
    
    # Get backend connection from pool
    backend_conn = connection_pool.get_connection(backend_host, backend_port)

    try:
        # Continue forwarding data using the backend_conn...
        threading.Thread(target=forward_data, args=(conn, backend_conn)).start()
        threading.Thread(target=forward_data, args=(backend_conn, conn)).start()
    finally:
        # Return connection back to pool when done
        connection_pool.return_connection(backend_conn)

def start_server(config):
    private_key, _ = generate_keys()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", config["listen_port"]))
        s.listen()
        logger.info(f"Server listening on port {config['listen_port']}")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr, private_key)).start()
