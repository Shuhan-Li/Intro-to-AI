"""
Client program


How To Run
------------

python3 Client.py -p <a port number> [-s server ip]

E.g. 
python3 Client.py -p 1234 -s 192.168.1.10       # connect server at 192.168.1.10 port 1234
python3 Client.py -p 1234 -s raspberrypi.local  # connect server at raspberrypi.local port 1234
python3 Client.py -p 1234                       # connect server at 127.0.0.1 port 1234

"""

import argparse
import socket
import json
import re
import math
import Number_Package as npkg
import random

#########Fill your RSA implementation here from Lab5.2########


def RSA_keygen():
    gap = random.randint(2**27, 2**29)

    # your code to implement RSA_keygen
    p = npkg.find_prime_smaller_than_k(2 ** 31 - gap)  # < the first prime number by seeking down from 2**31-gap
    q = npkg.find_prime_greater_than_k(2 ** 31 + gap)  # < the first prime number by seeking up from 2**31-gap
    e = 65537  # 65537 is a typical selection of e
    N = p * q
    phi = (p - 1) * (q - 1)
    d = npkg.mult_inv_mod_N(e, phi)


    return e, d, N


def RSA_decrypt(c, d, N):

    # your code to implement RSA_decrypt
    m = npkg.exp_mod(c, d, N)

    return m

##############################################################


def bytearray_xor(key, msg_bytes):
    # this is not a good encryption method, but it's a way :)

    # key to bytes
    key_bytearray = key.to_bytes(math.ceil(math.log2(key)), byteorder="big")

    key_len, msg_len = len(key_bytearray), len(msg_bytes)

    return bytearray(msg_bytes[i] ^ key_bytearray[i % key_len] for i in range(msg_len))

##############################################################


# def is_valid_ip(ip):
#     # check whether input ip is of IPV4
#     m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
#     return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))


parser = argparse.ArgumentParser(description='Lab5.3 Client Program')
parser.add_argument("-s", "--server", type=str, default="127.0.0.1",
                    help="A string of server IP (default: 127.0.0.1)")
parser.add_argument("-p", "--port", type=int,
                    help="port of the server to connect", required=True)
args = parser.parse_args()

# get the ip and port of the server
ip = args.server
port = args.port

# check whether input ip address is valid
# if is_valid_ip(ip):
#     print("Trying to connect to %s:%d" % (ip, port))
# else:
#     raise Exception("Invalid IP address")

print("Trying to connect to %s:%d" % (ip, port))

try:
    ################# write your code after this line############################

    s = socket.socket()

    # connect to server with input ip and port
    s.connect((ip, port))

    # generate public and private keys
    e, d, N = RSA_keygen()

    # send public keys to the server
    tdata = {'N': N, 'e': e}
    # send tdata to the server. 
    s.send(json.dumps(tdata).encode())

    # receive server's cipher (an integer)
    rdata_bytes = s.recv(1024)
    rdata = json.loads(rdata_bytes.decode())
    c = rdata["c"]

    # decrypt cipher
    key = RSA_decrypt(c, d, N)
    print("Server's key:", key)

    # for real applications, "m" can be treated as an initial key to encrypt the following transmission by choosing DES, tri-DES, AES, etc.
    # encrypt following message using provided bytearray_xor()
    plaintext = "This is the client. Let's follow your selected key to communicate!"
    ciphertext_bytes = bytearray_xor(key, plaintext.encode()) #< encrypt the message based on the key

    # send ciphertext_bytes to the server
    #s.send(json.dumps({"ciphertext": list(ciphertext_bytes)}).encode())
    s.send(ciphertext_bytes)

    # receive server's reply
    rciphertext_bytes = s.recv(1024)
    rplaintext_bytes = bytearray_xor(key, rciphertext_bytes)
    print("server msg:", rplaintext_bytes.decode())

    ################# write your code before this line############################
except ConnectionRefusedError:
    print("Connection refused. You need to run server program first.")
finally:
    s.close()
