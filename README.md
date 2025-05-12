# Secure-Proxying-Forwarding-using-Asymmetric-Encryption
A client-server app that can securely forward TCP communication over the internet using asymmetric encryption .

## Features

- Asymmetric key encryption with RSA (2048-bit)
- Simple binary protocol with handshake
- Logs and debug info using a shared logger

# Folder Structure

secure_proxy/

├── client/

│   ├── main.py          # Client script

│   ├── tunnel.py        # Handles local <-> server forwarding

│   ├── crypto_utils.py  # RSA key generation, encryption/decryption

│   └── config.py        # Configs like local port, server address

├── server/

│   ├── main.py          # Server script (public-facing)

│   ├── handler.py       # Handles each client socket

│   ├── crypto_utils.py  # Same as above, but on server side

│   └── config.py        # Server port, allowed clients

├── shared/

│   ├── protocol.py      # Defines commands/formats (HANDSHAKE, FORWARD, PING, EOF)

│   └── logger.py        # Shared logging util

├── README.md

├── requirements.txt

└── .env                 

# Encryption Flow 

1. Client generates RSA keypair 

2. On connect, client sends public key (HANDSHAKE_INIT).

3. Server responds with its public key (HANDSHAKE_RESPONSE).

4. All subsequent communication is encrypted using the other's public key


## Usage

1. Run server: `python server/main.py`
2. Run client: `python client/main.py`

Keys are generated automatically when the client starts and saved to disk.