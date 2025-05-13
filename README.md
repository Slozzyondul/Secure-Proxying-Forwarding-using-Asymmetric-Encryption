# Secure-Proxying-Forwarding-using-Asymmetric-Encryption
A client-server app that can securely forward TCP communication over the internet using asymmetric encryption .

# What Is Asymmetric Encryption?

Asymmetric encryption uses two keys:

- Public Key (shareable) — used to encrypt

- Private Key (secret) — used to decrypt

In the tunnel:

- Client encrypts the data using the server’s public key

- Server decrypts it using its private key

- This keeps data safe even if someone sniffs the traffic — they can't decrypt it without the private key.

# Steps	
1️⃣	Generate RSA keys (private + public)

2️⃣	Client encrypts messages with pubkey

3️⃣	Server decrypts using private key

4️⃣	Wrap it cleanly into the tunnel flow

# Hybrid Encryption Flow
AES is used for encrypting the main data (fast + secure).

RSA is used to encrypt the AES key (secure key exchange).

- The client sends:

RSA_ENCRYPTED_AES_KEY || AES_ENCRYPTED_DATA

- The server:

Extracts and decrypts the AES key using RSA.

Decrypts the rest of the data using AES.

# 🔁 Workflow:
1. Client → Encrypt request with server's public key → send.

2. Server → Decrypt request with private key.

3. Server → Forward to remote (e.g., example.com).

4. Server → Encrypt response with client's public key.

5. Client → Decrypt response with its private key.

# Generally

✅ Server starts and listens.

✅ Client connects and sends its public key.

✅ Server receives the public key.

✅ Client sends encrypted HTTP request.

✅ Server decrypts it, forwards to example.com, gets response.

✅ Server encrypts the response, sends it back to client.

✅ Client decrypts and prints the response.



- The client sends its public key to the server during initial handshake.


## Usage

Run it once:

1. Generate keys: At the root of the project, run `PYTHONPATH=. python3 keys/generate_keys.py`

You’ll get:

keys/private_key.pem

keys/public_key.pem

# Start server and client:

1. Run server: At the root of the project, run `PYTHONPATH=. python3 server/main.py`
2. Run client: At the root of the project, run `python3 client/client.py`

