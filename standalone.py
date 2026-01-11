from core import DiffieHellman

# public parameters
p, g = 23, 5

alice = DiffieHellman(p, g)
bob = DiffieHellman(p, g)

alice_secret = alice.get_shared_secret(bob.public_key)
bob_secret = bob.get_shared_secret(alice.public_key)

print("Alice public:", alice.public_key)
print("Bob public:", bob.public_key)
print("Alice secret:", alice_secret)
print("Bob secret:  ", bob_secret)
