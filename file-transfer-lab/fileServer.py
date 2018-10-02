#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import os, socket, params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()
    from framedSock import framedSend, framedReceive
    
    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            payload = framedReceive(sock, debug)
            if not payload:
                sys.exit(0)
            return_message = payload
            split_payload = payload.decode().split(' ')
            if split_payload[0] == 'put':
                write_file = True
                if os.path.isfile(split_payload[1]):
                    framedSend(sock, b'overwrite', debug)
                    choice = framedReceive(sock, debug)
                    if not choice:
                        sys.exit(0)
                    if choice != b'y':
                        write_file = False
                else:
                    framedSend(sock, b'', debug)
                if write_file:
                    file_name = framedReceive(sock, debug)
                    file_contents = framedReceive(sock, debug)
                    if not file_name:
                        sys.exit(0) 
                    if file_name and file_contents:
                        if os.path.isfile(file_name.decode()): #rename_file
                            file_name = file_name.decode().split('.')
                            file_name[-2] = file_name[-2] + '_copy'
                            file_name = '.'.join(file_name)
                        f = open(str(file_name), 'w')
                        f.write(str(file_contents.decode()))
                        f.close()
                        return_message = b'Transfer Successful!'
                    else:
                        return_message = b'Transfer Cancelled!'
                else:
                    return_message = b'Transfer Cancelled!'
            framedSend(sock, return_message, debug)
