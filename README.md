**Title: Diffie-Hellman Secret Chat – Python 🔐**

This project is a tiny, crazy-looking demo of how two people can talk **secretly** over a totally insecure channel just by doing some smart logical math – the Diffie-Hellman (DH) key exchange.  

Once the key is agreed, the messages are “scrambled” with that key, so anyone sniffing the network sees only gibberish.

***

## What this project shows

- How two parties (Alice and Bob) generate a shared secret key **without ever sending the secret itself**.  
- How that shared secret can be used to encrypt and decrypt messages over a normal TCP connection.  
- That pure math (modular exponentiation + random numbers) is enough to build a private communication channel.

At a high level:

1. Alice and Bob agree on public numbers \( p \) and \( g \).  
2. Each picks a private number (never shared).  
3. Each sends a corresponding public value.  
4. Using the other’s public value and their own private one, both compute the **same** shared secret key.  
5. That key is then used to XOR‑encrypt chat messages, turning normal text into apparently random symbols.

Anyone watching the traffic sees only encrypted junk, but Alice and Bob see normal text.

***

## Project structure

```text
DH Key/
├── core.py        # DiffieHellman class and modular exponentiation
├── standalone.py  # Simple Alice–Bob DH demo in one script
├── server.py      # “Bob” – waits for connection, chats using shared key
├── client.py      # “Alice” – connects to Bob, chats using shared key
```

### core.py

Contains:

- `mod_pow(base, exp, mod)`: efficient modular exponentiation.  
- `DiffieHellman` class:
  - Random private key.
  - Public key \( g^{\text{private}} \mod p \).
  - Method to compute the shared secret from the other party’s public key.

This file is pure logic/math – no networking.

### standalone.py

Quick local sanity check:

- Creates Alice and Bob objects.  
- Prints their public keys and shared secrets.  
- Verifies that both secrets are identical.

Example output:

```text
Alice public: 11
Bob public: 18
Alice secret: 12
Bob secret:  12
```

***

## How the secret chat works

The chat is implemented with Python sockets and the DH key:

- `server.py` (Bob):
  - Listens on a TCP port.
  - Sends its public key to the client.
  - Receives Alice’s public key.
  - Computes the shared secret.
  - Uses that secret to encrypt/decrypt messages.

- `client.py` (Alice):
  - Connects to the server.
  - Receives Bob’s public key.
  - Sends its own public key.
  - Computes the same shared secret.
  - Uses it to encrypt/decrypt messages.

Encryption is done via a simple XOR with the shared key (mod 256) – not production‑grade crypto, but perfect to **visualize** how a shared secret can drive message scrambling and unscrambling.

***

## How to run (local machine)

1. Clone the repo and go into the folder:

```bash
git clone <your-repo-url>.git
cd "DH Key"
```

2. Test the math:

```bash
python3 standalone.py
```

You should see Alice and Bob end up with the same secret.

3. Open **two terminals**.

- Terminal 1 – start the server (Bob):

```bash
cd ~/Desktop/"DH Key"   # or the folder path you use
python3 server.py
```

- Terminal 2 – start the client (Alice):

```bash
cd ~/Desktop/"DH Key"
python3 client.py
```

4. Start chatting:

- Type in Bob’s terminal → decrypted in Alice’s.  
- Type in Alice’s terminal → decrypted in Bob’s.  
- Type `quit` to exit.

***

## Running over the internet

The same “secret math chat” can work across different networks:

- On the **server**, listen on all interfaces and use a public/LAN IP instead of `localhost`.  
- On the **client**, replace `HOST = 'localhost'` with the server’s IP.  
- Configure router port forwarding and allow the port in firewalls.

After that, you essentially have a tiny, hand‑rolled, math‑based secret messenger.

***

## Why this is cool (and a little crazy)

- No pre‑shared password. The secret key *emerges* from the math during the exchange.  
- Anyone can see \( p \), \( g \), Alice’s public value, and Bob’s public value – yet computing the secret from those alone is computationally hard.  
- This is the same core idea behind how modern secure protocols (like HTTPS and many VPNs) agree on keys before encrypting data.

So this project is more than just four Python files – it’s a minimal, understandable, “from scratch” version of the logical math that powers real‑world secure communication.

***

## Possible extensions

- Replace XOR with a proper symmetric cipher (AES) using the shared secret.  
- Add a simple GUI (Tkinter) for chat.  
- Log the raw encrypted traffic to show how unreadable it looks without the key.  
- Add a “fake attacker” mode to demonstrate man‑in‑the‑middle risks.

***
