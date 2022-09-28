#!/usr/bin/env python3

import socket
import time
from getmac import get_mac_address as gma

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Enable port reusage so we will be able to run multiple clients and servers on single (host, port).
# Do not use socket.SO_REUSEADDR except you using linux(kernel<3.9): goto https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ for more information.
# For linux hosts all sockets that want to share the same address and port combination must belong to processes that share the same effective user ID!
# So, on linux(kernel>=3.9) you have to run multiple servers and clients under one user to share the same (host, port).
# Thanks to @stevenreddie
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Enable broadcasting mode
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)

""" COMMAND_ALERT : 142
body: servermac-state-deviceid-type
state = 0 : Off
state = 1: On
type = 1: fire
type = 2: warning
device: MAC-device || ALL
 """
NEW_SOCKET_COMMAND_HEADER=8899
COMMAND=142
REQUEST_ID=0

MAC_ADDRESS = gma()
STATE='1'
DEVICE_ID='all'
TYPE='1'

body = f"{MAC_ADDRESS}-{STATE}-{DEVICE_ID}-{TYPE}"

def initBodyMessage(NEW_SOCKET_COMMAND_HEADER, command, body, requestId):
    bodyLength = len(body)

    buff_0 = NEW_SOCKET_COMMAND_HEADER & 0xff
    buff_1 = NEW_SOCKET_COMMAND_HEADER >> 8 & 0xff
    buff_2 = command & 0xff
    buff_3 = command >> 8 & 0xff
    buff_4 = requestId & 0xff
    buff_5 = requestId >> 8 & 0xff
    buff_6 = requestId >> 16 & 0xff
    buff_7 = requestId >> 24 & 0xff
    buff_8 = bodyLength & 0xff
    buff_9 = bodyLength >> 8 & 0xff
    buff_10 = bodyLength >> 16 & 0xff
    buff_11 = bodyLength >> 24 & 0xff
    return bytes([buff_0, buff_1, buff_2, buff_3, buff_4, buff_5, buff_6, buff_7, buff_8, buff_9, buff_10, buff_11])
message = initBodyMessage(NEW_SOCKET_COMMAND_HEADER, COMMAND, body, REQUEST_ID)
print(message)
message +=(str.encode(body))

while True:
    server.sendto(message, ("192.168.1.255", 37020))
    print("message sent!", flush=True)
    time.sleep(1)

