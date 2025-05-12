import struct

HANDSHAKE_INIT = 0x10
HANDSHAKE_RESPONSE = 0x11

def pack_handshake_init(public_key_bytes):
    return struct.pack("!B", HANDSHAKE_INIT) + public_key_bytes

def unpack_handshake_init(data):
    return data[1:]  # remove the command byte

def pack_handshake_response(encrypted_token):
    return struct.pack("!B", HANDSHAKE_RESPONSE) + encrypted_token

def unpack_handshake_response(data):
    return data[1:]
