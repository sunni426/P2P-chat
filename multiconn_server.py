import sys
import socket
import selectors
import types

'''
    handles multiple connections using a selector objects reated from selectors module
    source: https://realpython.com/python-sockets/#multi-connection-client-and-server 
    run: python multiconn_server.py 127.0.0.1 65432
        arguments: addr, port #
'''

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False) # main objective: don't want server to block
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data) # now, should be ready to read. registers socket


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

    
# set up listening socket
host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False) # configures socket in non-blocking mode (calls made will no longer block), 
# so can wait for events on 1+ sockets & read/write data when ready
sel.register(lsock, selectors.EVENT_READ, data=None) # registers sockets to be monitored with sel.select(). read events


# event loop
try:
    while True:
        events = sel.select(timeout=None) # blocks until there are sockets ready for I/O
        for key, mask in events:
            if key.data is None: # so is from listening socket, accept connection
                accept_wrapper(key.fileobj)
            else: # it’s a client socket that’s already been accepted, and you need to service it
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
