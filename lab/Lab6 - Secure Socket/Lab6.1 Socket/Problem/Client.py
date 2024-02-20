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

# Since hostname is also supported, so this function is not necessary
# def is_valid_ip(ip):
#     # check whether input ip is of IPV4
#     m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
#     return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))


parser = argparse.ArgumentParser(description='Lab6.1 Client Program')
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

msg = b''
try:
    ################# write your code after this line############################
    s = socket.socket()

    # connect to server with input ip and port
    s.connect((ip,port)) #< your code here

    # message transmission
    # send "Hello Server" to the server
    tmsg = "Hello Server"
    s.send(tmsg.encode(encoding="UTF-8"))

    # receive server's reply (a bytearray)
    rmsg_byte = s.recv(1024)  #< change to an appropriate function
    rmsg = rmsg_byte.decode(encoding="UTF-8")
    print("Server: ", rmsg)

    # structured data transmission
    # send sdata to the server (hint: use json to transfer back and forth between structured data and bytes)
    # public key of RSA with p:2127836173 q:2167131101 d:855599238897129473
    tdata = {'N': 4611299948341116473, 'e': 65537}
    tdata_byte = json.dumps(tdata).encode(encoding="UTF-8") #< python dictionary to byte conversion. 
                            #< you can use your way to do the conversion. For example, json.dump, or the "to_bytes" function
    s.send(tdata_byte)      #< send the byte array to the server

    # receive server's data (check Server.py for detail)
    rdata_byte = s.recv(1024) #< receive byte array from the socket
    c = json.loads(rdata_byte.decode(encoding="UTF-8")) #< interpret the byte array
    print("Server: ", c)    #< print the cipher sent by the server

    ################# write your code before this line############################
except ConnectionRefusedError:
    print("Connection refused. You need to run server program first.")
finally:
    s.close()
