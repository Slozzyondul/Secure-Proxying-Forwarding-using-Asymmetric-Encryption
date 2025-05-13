# client/test_client.py

import socket

def main():
    host = "127.0.0.1"  # local tunnel server
    port = 9999         # Same port as the tunnel

    try:
        with socket.create_connection((host, port)) as sock:
            # Send an HTTP GET request through the tunnel
            request = b"GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"
            sock.sendall(request)

            # Receive and print the response
            response = b""
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                response += data

            print(response.decode(errors="replace"))

    except Exception as e:
        print(f"[!] Client error: {e}")

if __name__ == "__main__":
    main()
