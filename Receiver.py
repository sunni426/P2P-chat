import socket
import sys
import threading
from discovery import *

def handle_client(client_socket, client_address, username, discovery_module):
    """Handle a client connection."""

    while True:
        try:
            # receive message from the client
            message = client_socket.recv(1024)
            if message:
                print(message.decode('utf-8'))
            # broadcast the message to all clients
            # message = input()
            # client_socket.send(message.encode('utf-8'))
        except KeyboardInterrupt:
            discovery_module.setUserOffline(username)
            client_socket.close()
            sys.exit(0)
        except Exception as e:
            print(f'Client {client_address} disconnected')
            discovery_module.setUserOffline(username)
            client_socket.close()
            #call the updateOffline function
            break


if __name__ == "__main__":
    discovery_api_host = input("Enter discovery_api server's host: ")
    discovery_api_port = input("Enter discovery_api server's port: ")
    discovery = Discovery(discovery_api_host, discovery_api_port)
    name = input("Enter your username: ")
    if not discovery.checkUserExists(name):
        print("You don't exists in the database. Now we are creating a new account for you.")
        SELF_HOST = input("Enter your host: ")
        SELF_PORT = int(input("Enter your port: "))
        discovery.insertUser(name, "online", SELF_HOST, SELF_PORT)
    else:
        SELF_HOST = input("Enter your host: ")
        SELF_PORT = int(input("Enter your port: "))
        discovery.updateIpAndPort(name, SELF_HOST, SELF_PORT)

    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to a public host and a port
    server_socket.bind((SELF_HOST, SELF_PORT))

    # listen for incoming connections
    server_socket.listen()
    print("You are online. Waiting for other users to connect to you...")

    client = None

    while True:
        # accept a client connection
        try:
            client_socket, client_address = server_socket.accept()

            # start a new thread to handle the client connection
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, name, discovery))
            client_thread.start()
            # discovery.setUserOffline(name)
            # sys.exit(0)
        except KeyboardInterrupt:
            print("keyboard interruption")
            discovery.setUserOffline(name)
            client_socket.close()
            sys.exit(0)
        except Exception as e:
            print("Error: "+ str(e))
            discovery.setUserOffline(name)
            client_socket.close()
            sys.exit(0)

