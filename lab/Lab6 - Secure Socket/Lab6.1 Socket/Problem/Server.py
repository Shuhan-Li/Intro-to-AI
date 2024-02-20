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
import re
import json


parser = argparse.ArgumentParser(description='Lab5.1 Server Program')
parser.add_argument("-p", "--port", type=int, \
                    help="port of the server to connect", required=True)
args = parser.parse_args()

# get the ip and port of the server
port = args.port


try:
    
    ################# write your code after this line############################

    s = socket.socket()
    
    # bind to input port
    s.bind(("", port)) #< your code here 172.29.128.1

    print("Server is listening to port %d" %(port))

    # put at most 2 connections in backlog (or say 3 connections at most). Refuse more connections
    s.listen(2) #< your code here

    msg = b''
    addr=''

    while True: 
        print("="*30)
        print("waiting for connection")
        # Establish connection with client, where c is the connection handler and addr is the client's ip
        c, addr = s.accept() #< your code here
        print ('Got connection from', addr)

        ## message transmission
        # receive message from the client
        rmsg_bytes = c.recv(1024) #< receive the welcome message but in byte array
        rmsg = rmsg_bytes.decode("UTF-8") #< convert byte array to char string
        print("client: ", rmsg)

        # reply the client with tmsg
        tmsg = 'Hello, this is the server'
        c.send(tmsg.encode(encoding="UTF-8")) #< send the server reply to the client


        ## data transmission 
        rdata = json.loads(c.recv(1024).decode(encoding="UTF-8")) #< necessary codes to process the RSA parameter from the client
        e = rdata["e"] #< interpret the e from the received data
        N = rdata["N"] #< interpret N
        print("client e: ", e)
        print("client N: ", N)


        # We will focusing on generating the key in the next section.
        # Here, we temporarily use the cipher that is provided reply 
        tdata = {'c':2438923152802212086}  # c is a RSA cipher
        c.send(json.dumps(tdata).encode(encoding="UTF-8")) #< send the cipher to the client
        # Close the connection with the client 
        c.close() 

    ################# write your code before this line############################
except ConnectionRefusedError:
    print("Connection refused. You need to run server program first.")
finally: # must have
    print("free socket")
    s.close()
