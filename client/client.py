import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.encryption import load_public_key, encrypt_message
from utils.decryption import load_private_key, decrypt_message
import socket

def main():
    host = "127.0.0.1"  # local tunnel server
    port = 9999         # Same port as the tunnel
    public_key = load_public_key()

    # Load client's own keys
    public_key = load_public_key("keys/public_key.pem")  
    private_key = load_private_key("keys/private_key.pem") 

    try:
        with socket.create_connection((host, port)) as sock:
             # Step 1: Send public key to server
            with open("keys/public_key.pem", "rb") as f:
                pubkey_data = f.read()
                sock.sendall(pubkey_data)
                
           # Step 2: Prepare HTTP request and encrypt
            request = b"GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"
            encrypted_data = encrypt_message(request, public_key)  # Optional: you could encrypt with server pubkey instead if hybrid
            sock.sendall(encrypted_data)
              
            # Step 3: Receive and decrypt the response
            decrypted_response = b""
            while True:
                data = sock.recv(4096)
                if not data:
                    break           

                try:
                    decrypted_chunk = decrypt_message(data, private_key)
                    decrypted_response += decrypted_chunk 
                    
                except Exception as e:
                    print(f"[!]  Failed to decrypt chunk: {e}")
                    break
            print(decrypted_response.decode(errors="replace"))

    except Exception as e:
        print(f"[!] Client error: {e}")

if __name__ == "__main__":
    main()
