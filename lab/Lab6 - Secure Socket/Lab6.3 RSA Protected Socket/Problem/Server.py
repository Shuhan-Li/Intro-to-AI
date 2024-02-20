"""
Server program

How To Run
------------

python3 Server.py -p <a port number>

E.g. 
python3 Server.py -p 1234                       # server listen to port 1234


"""

import argparse
import socket
import json
import re
import Number_Package as npkg
import random
import math

#########Fill your RSA implementation here from Lab5.2########

def RSA_encrypt(m, e, N):
    
    # your code to implement RSA_encrypt
    c = npkg.exp_mod(m, e, N)

    return c

# we provide you with a byte-wise XOR encryption method. 
# The idea is to XOR one key byte with one msg byte one by one.
def bytearray_xor(key, msg_bytes):
    # key is an integer                             e.g. 42311000090981230
    # msg_bytes is a byte string (or bytearray).    e.g. b'Hello world'
    key = int(key)
    
    key_bytearray = key.to_bytes(math.ceil(math.log2(key)), byteorder="big")
    
    key_len, msg_len = len(key_bytearray), len(msg_bytes)

    return bytearray(msg_bytes[i] ^ key_bytearray[i%key_len] for i in range(msg_len))
        
##############################################################

parser = argparse.ArgumentParser(description='Lab6.3 Server Program')
parser.add_argument("-p", "--port", type=int, \
                    help="port of the server to connect", required=True)
args = parser.parse_args()

# get the ip and port of the server 
port = args.port

s = socket.socket()
s.bind(('', port)) 
print("Server is listening to port %d" %(port))

try:
    
    ################# write your code after this line############################

    
    # put at most 2 connections in backlog (or say 3 connections at most). Refuse more connections
    s.listen(2)

    while True: 
        print("="*30)
        print("waiting for connection")
        
        # Establish connection with client, where c is the connection handler and addr is the client's ip
        c, addr = s.accept()
        print ('Got connection from', addr)

        # receive client's public keys 'e' and 'N'
        rdata_bytes = c.recv(1024)
        # use json to parse the receive data 
        rdata = json.loads(rdata_bytes.decode())
        
        e, N = rdata['e'], rdata['N']

        # randomly choose a key 
        key = random.randint(0, N)
        print("server chooses key:", key)

        # encrypt m
        tdata = {'c':RSA_encrypt(key, e, N)}
        # send tdata to the client
        c.send(json.dumps(tdata).encode())

        # for real applications, "m" can be treated as an initial key to encrypt the following transmission by choosing DES, tri-DES, AES, etc.
        # 
        ciphertext_bytes = c.recv(1024)
        plaintext_bytes = bytearray_xor(key, ciphertext_bytes)
        print("Client msg:", plaintext_bytes.decode("UTF-8"))#list(plaintext_bytes))#

        # server sends a reply message
        plaintext = "Hello, this is the server."
        ciphertext_bytes = bytearray_xor(key, plaintext.encode())         #< your code to convert plaintext to bytes and then generate the cipher "ciphertext_bytes"
        c.send(ciphertext_bytes)


        # Close the connection with the client 
        c.close() 

    ################# write your code before this line############################
except ConnectionRefusedError:
    print("Connection refused. You need to run server program first.")
finally: # must have
    print("free socket")
    s.close()
