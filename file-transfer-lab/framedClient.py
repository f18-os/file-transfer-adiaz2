#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50007"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

while True:
    message = input('>>>')
    split_message = message.split(' ')
    if split_message[0] == 'put':
        if os.path.isfile(split_message[1]):
            framedSend(s, bytes(message, 'utf-8'), debug)
            error = framedReceive(s, debug)
            write_file = True
            if error == b'overwrite':
                while(True):
                    overwrite = input('This file already exists, overwrite the current file? (y/n)\n')
                    if overwrite == 'y':
                        break
                    elif overwrite == 'n':
                        write_file = False
                        break
                framedSend(s, bytes(overwrite, 'utf-8'), debug)
            if write_file:
                f = open(split_message[1], 'r')
                contents = f.read()
                f.close()
                message = split_message[1] + ':::' + contents
    b_message = bytes(message, 'utf-8')
    framedSend(s, b_message, debug)
    print(b_message)
    framedSend(s, b_message, debug)
    print("received:", framedReceive(s, debug))
        
    
