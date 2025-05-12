# Secure-Proxying-Forwarding-using-Asymmetric-Encryption
A client-server app that can securely forward TCP communication over the internet using asymmetric encryption .

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

│   ├── protocol.py      # Defines commands/formats

│   └── logger.py        # Shared logging util

├── README.md

├── requirements.txt

└── .env                 
