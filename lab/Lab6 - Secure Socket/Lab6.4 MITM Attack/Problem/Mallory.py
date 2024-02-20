"""
Mallory program (The malicious active attacker who conducts the MITM attack)

How To Run
------------

python3 Mallory.py -p <server port> -s <server ip> -c <spoofied port for client>

E.g. 
python3 Mallory.py -p 1234 -s 127.0.0.1 -c 12345      #


"""

import argparse
import socket
import json
import re
import Number_Package as npkg
import math
import random

#########Fill your RSA implementation here from Lab5.2########


def RSA_encrypt(m, e, N):
    c = pow(m, e, N)
    return c


def RSA_keygen():
    gap = random.randint(2 ** 27, 2 ** 29)

    # your code to implement RSA_keygen
    p = npkg.find_prime_smaller_than_k(2 ** 31 - gap)  # < the first prime number by seeking down from 2**31-gap
    q = npkg.find_prime_greater_than_k(2 ** 31 + gap)  # < the first prime number by seeking up from 2**31-gap
    e = 65537  # 65537 is a typical selection of e
    N = p * q
    phi = (p - 1) * (q - 1)
    d = npkg.mult_inv_mod_N(e, phi)
    return e, d, N


def RSA_decrypt(c, d, N):
    m = pow(c, d, N)
    return m

#


def bytearray_xor(key, msg_bytes):
    key_bytearray = key.to_bytes(math.ceil(math.log2(key)), byteorder="big")

    key_len, msg_len = len(key_bytearray), len(msg_bytes)

    return bytearray(msg_bytes[i] ^ key_bytearray[i % key_len] for i in range(msg_len))

##############################################################


parser = argparse.ArgumentParser(description='Lab6.4 Mallory Program')
parser.add_argument("-p", "--serverport", type=int,
                    help="port of the server to connect", required=True)
parser.add_argument("-s", "--server", type=str, default="127.0.0.1",
                    help="A string of server IP (default: 127.0.0.1)")
parser.add_argument("-c", "--clientport", type=int,
                    help="port for clients to connect", required=True)
args = parser.parse_args()

# get the ip and port of the server
server_port = args.serverport
server_ip = args.server
client_port = args.clientport


s_svr = socket.socket()  # socket to connect to the server
s_clt = socket.socket()  # socket to open to the client (victim)

s_clt.bind(('', client_port))
print("Mallory is listening to port %d" % (client_port))

try:

    ################# write your code after this line############################

    # put no connections in backlog (or say 3 connections at most). Refuse more connections
    s_clt.listen(0)

    while True:
        print("="*30)
        print("waiting for victim to connect")
        # Establish connection with client.

        """deal with the connected victim"""
        c, addr = s_clt.accept()
        print('Got connection from victim', addr)

        # receive client's public keys 'e' and 'N'
        rdata_bytes = c.recv(1024)
        rdata = json.loads(rdata_bytes.decode())

        e4vic, N4vic = rdata['e'], rdata['N']

        """build up the connection to the real server"""
        # connect to the real server
        s_svr.connect((server_ip, server_port))

        # generate a new set of keys to communicate with the server
        e4svr, d4svr, N4svr = RSA_keygen() # generate the (e, d, N) for the server

        # send public keys to the server
        tdata = {'N': N4svr, 'e': e4svr}
        s_svr.send(json.dumps(tdata).encode())         # send the public keys to the server

        # receive server's cipher
        rdata_bytes = s_svr.recv(1024)
        rdata = json.loads(rdata_bytes.decode())
        c4svr = rdata['c']

        # decrypt out server's selected key
        key = RSA_decrypt(c4svr, d4svr, N4svr)  # decrypt the key chosen by the server
        print("Server's key:", key)

        # encrypt key and send to the victim (client)
        tdata = {'c': RSA_encrypt(key, e4vic, N4vic)}  
        # send tdata to the victim
        c.send(json.dumps(tdata).encode())#!!!!

        """So far, Mallory has acquired the key and set up connections to both the real server and the victim client."""
        # get the victim's message, decrypt and then encrypt using server's key and send out
        ciphertext_from_victim_bytes = c.recv(1024)
        plaintext_from_victim_bytes = bytearray_xor(
            key, ciphertext_from_victim_bytes)
        print("Victim -> Server:", plaintext_from_victim_bytes.decode())
        # send to the server
        s_svr.send(ciphertext_from_victim_bytes)

        # receive server's reply, decrypt the ciphertext locally to get the message
        ciphertext_from_server_bytes = s_svr.recv(1024)
        plaintext_from_server_bytes = bytearray_xor(
            key, ciphertext_from_server_bytes)
        print("Server -> Client:", plaintext_from_server_bytes.decode())
        # send client the received ciphertext
        c.send(ciphertext_from_server_bytes)

        # Close the connection with the client and the server
        c.close()
        s_svr.close()

    ################# write your code before this line############################
except ConnectionRefusedError:
    print("Connection refused. You need to run server program first.")
finally:  # must have
    print("free socket")
    s_clt.close()
    s_svr.close()
