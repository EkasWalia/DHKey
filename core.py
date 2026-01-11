import random

def mod_pow(base, exp, mod):
    """Efficient modular exponentiation."""
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result


class DiffieHellman:
    def __init__(self, p, g):
        self.p = p  # Large prime
        self.g = g  # Generator
        self.private_key = random.randint(2, p - 2)
        self.public_key = mod_pow(g, self.private_key, p)
    
    def get_shared_secret(self, other_public):
        return mod_pow(other_public, self.private_key, self.p)
