#!/usr/bin/env python3

# numpy has been noticed to have a different implementation on 32 and 64 bit machine. 
# We are trying to avoid that and use "random" packet. 
# import numpy as np 
import random
import Number_Package as npkg  # this is a package you will use (script with useful functions)

"""
Bob needs to send a message (a randomly chosen number) to Alice via a public unsecure channel.
Alice and Bob decide to choose public cryptography method - RSA.
Your task is to follow the instruction in the comments to complete the missing parts.
"""

"""
Step 1:
Alice first generates 
    private components (p, q, d) and public components (e, N)

Requirements:
1. The selection of p and q should both be 
    1) relatively large 
    2) random 
    3) not close to each other. 

We suggest you to choose p and q at around 2**31 +/- a gap, i.e. p <= 2**31 - gap and q >= 2**31+gap. Code for gap is there.

2. A typical selection of e is 65537. This selection is widely accepted by many RSA implementation, such as openssl.
"""
gap = random.randint(2**27, 2**29) # 

p = npkg.find_prime_smaller_than_k(2**31 - gap)  #< the first prime number by seeking down from 2**31-gap
q = npkg.find_prime_greater_than_k(2**31 + gap)  #< the first prime number by seeking up from 2**31-gap
e = 65537 # 65537 is a typical selection of e

# follow the RSA algorithm
N = 4400141856896539081#p*q
phi = (p - 1) * (q - 1)
d = 2764011776369096961#npkg.mult_inv_mod_N(e, phi)

print("Alice choose:\np:{p}\nq:{q}\nN:{N}\ne:{e}\nd:{d}".format(p=p, q=q, N=N, e=e, d=d))

"""
Step 2:
Alice sends (N, e) to Bob

Notes:
For this lab, you DON'T need to write anything here. This will be integrated into the socket example in the next section. 
"""
# This task is done magically in this section.

"""
Step 3:
Bob uses the received (N, e)
"""
m = 000000#random.randint(0, N) # a randomly chosen message in GF(N). You can replace this line with any desinated message in the future
c = 2503673653585535070#npkg.exp_mod(m, e, N)       # encrypt m
print("Bob chooses to encrypt plaintext:", m)
print("Bob sends ciphertext            :", c)

"""
Step 4:
Bob sends the encrypted message to Alice
For this lab, you DON'T need to write anything here. You can think about adding socket communication codes here in the future.
"""

"""
Step 5:
Alice uses her private key d to decrypt Bob's ciphertext.

Ideally, m = m_decrypt
"""
m_decrypt = npkg.exp_mod(c, d, N)    #< decrypt c with Alice's private keys
print("Alice decrypts Bob's msg and get:", m_decrypt)


