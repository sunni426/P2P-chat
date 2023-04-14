import sys
import socket
import selectors
import types
import select # for OS-level I/O capabilities
import errno

'''
    every user will "enter chat" by running this to establish a connection with another user.
    status will be updated in discovery_server [TO BE IMPLEMENTED BY SAM]
    127.0.0.1 the IP address of the local computer (localhost)
'''

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 65342

# this info will be sent to discovery_server, into socket list
my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
client_socket.setblocking(False)
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

# next, find target
target_user = input(f"SendTo: ")
targetuser = target_user.encode('utf-8')
targetuser_header = f"{len(targetuser):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(targetuser_header + targetuser)

# now, event loop. pending, idle chat status. to send & receive messages
while True:
    message = input(f"{my_username} > ")

    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        # now, send message
        client_socket.send(message_header + message)

    # try to receive all pending messages, with error checking
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Connection closed")
                sys.exit() # check if we want this or some other handling
            
            # get username info
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            # get message itself, coming in a stream. careful with size

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f"{username} > {message}")
    
    # if no more messages to receive. perhaps try  creating chat close functionality
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))

    except Exception as e:
        print('General error', str(e))
        sys.exit()
            