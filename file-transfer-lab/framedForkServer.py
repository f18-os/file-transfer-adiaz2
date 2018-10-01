#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import os, socket, params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50007),
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
            print(payload)
            if not payload:
                sys.exit(0)
            return_message = payload
            split_payload = payload.decode().split(' ')
            if split_payload[0] == 'put':
                write_file = True
                if os.path.isfile(split_payload[1]):
                    framedSend(sock, b'overwrite', debug)
                    print('overwrite sent')
                    choice = framedReceive(sock, debug)
                    print(choice)
                    if choice != b'y':
                        write_file = False
                else:
                    framedSend(sock, b'', debug)
                    print('no file found')
                if write_file:
                    print('awaiting file info')
                    file_info = framedReceive(sock, debug)
                    print('file_info ' + str(file_info))
                    if file_info:
                        print('file_info: ' + str(file_info))
                        split_file_info = file_info.decode().split(':::')
                        f = open(split_file_info[0], 'w')
                        f.write(split_file_info[1])
                        f.close()
                        return_message = b'Transfer Successful!'
                else:
                    print(write_file)
                    return_message = b'Transfer Cancelled!'
            print('return_message ' + str(return_message))
            framedSend(sock, return_message, debug)
