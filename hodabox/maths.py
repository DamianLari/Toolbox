import numpy as np


def decomposer_en_facteurs_premiers(n):
        facteurs = []
        while n % 2 == 0:
            facteurs.append(2)
            n //= 2
        facteur = 3
        
        while facteur * facteur <= n:
            while n % facteur == 0:
                facteurs.append(facteur)
                n //= facteur
            facteur += 2
            
        if n > 2:
            facteurs.append(n)

        return facteurs

def pgcd(a, b):
    while b:
        a, b = b, a % b
    return a

def ppcm(a, b):
    return abs(a * b) // pgcd(a, b)

def is_prime_number(n):
    return n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))
