import socket

'''
    hard code connections between them
    https://realpython.com/python-sockets/
    server: socket --> bind --> listen --> accept, connect w/ client: establishing connection, 3-way handshake
    client: socket --> connect, 3 way handshake

    think of each chat as an independent network
'''

# create a socket object
# s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM type: default protocol is TCP

HOST = "127.0.0.1"  # The server's hostname or IP address. The default internal loop IP for the localhost is usually 127.0. 0.1
PORT = 65432  # The port used by the server

# infinite loop over blocking calls to conn.recv: reads whatever data client sends, echoes it back using sendall
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept() # new socket object: to comm with client, DIFF from listening socket that server is using to accept new connections
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)