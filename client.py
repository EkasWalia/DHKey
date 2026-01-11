from core import DiffieHellman
import socket

p, g = 23, 5
HOST, PORT = 'localhost', 9999

alice = DiffieHellman(p, g)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Alice: connected to server")

    # receive Bob's public key
    bob_public = int(s.recv(1024).decode())

    # send Alice's public key
    s.send(str(alice.public_key).encode())

    shared = alice.get_shared_secret(bob_public)
    print(f"Alice shared secret: {shared}")

    while True:
        data = s.recv(1024)
        if not data:
            break
        dec = ''.join(chr(ord(c) ^ (shared % 256)) for c in data.decode())
        print("Bob:", dec)

        msg = input("Alice: ")
        if msg.lower() == "quit":
            break
        enc = ''.join(chr(ord(c) ^ (shared % 256)) for c in msg)
        s.send(enc.encode())
