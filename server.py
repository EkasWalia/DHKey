from core import DiffieHellman
import socket

p, g = 23, 5
HOST, PORT = 'localhost', 9999

bob = DiffieHellman(p, g)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Bob: waiting for connection...")
    conn, addr = s.accept()
    with conn:
        print("Bob: connected to", addr)

        # send Bob's public key
        conn.send(str(bob.public_key).encode())

        # receive Alice's public key
        alice_public = int(conn.recv(1024).decode())

        shared = bob.get_shared_secret(alice_public)
        print(f"Bob shared secret: {shared}")

        while True:
            msg = input("Bob: ")
            if msg.lower() == "quit":
                break
            enc = ''.join(chr(ord(c) ^ (shared % 256)) for c in msg)
            conn.send(enc.encode())

            data = conn.recv(1024)
            if not data:
                break
            dec = ''.join(chr(ord(c) ^ (shared % 256)) for c in data.decode())
            print("Alice:", dec)
