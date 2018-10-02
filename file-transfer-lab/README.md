# File Transfer Lab
This is a simple program that allows a Client to send files to a Server using
the 'put' command. If the Server already contains a file under that name, the
file will be stored as a copy. For example, if the Client tries to transfer a file
named 'something.txt' and a file with the same name already exists on the
Server, the file will be saved as 'something_copy.txt'.

The Server can support multiple clients at the same time through Forking.

The data is sent from the Client through a Proxy that forwards the data from
the Client to the Server. 

By default, the Proxy listens on port '50000' and the Client connects to the server at
port '50000', although these ports can be changed using the optional parameters
-l and -s respectively. This allows communication from the Client to the Proxy.

By default, the Server listens on port '50001' and the Proxy connects to the
server at port '50001', although these ports can also be changed using the
optional parameters -l and -s. This allows the Proxy to forward the messages
sent by the Client to the Server.

To run the client and server with the proxy on the same shell, use the
following command:

python3 fileServer.py & python3 stammerProxy.py & python3 fileClient.py

This will run the Server and the Proxy as background processes and the Client
as a foreground process. This will allow you to type in commands as the Client
to the Server.

Once the client is open, type in:

put path/to/directory/file_name

As long as the file is valid, the file will be transferred to the Server.
