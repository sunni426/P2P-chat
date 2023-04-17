import socket
import sys
import threading
from discovery import *
from sqlite3_database import *

# define server IP address and port


def send(discovery_module, self_user, target_name, original_host, original_port, given_socket):
    conn = given_socket
    #user is online:
    greeting_msg = "{user} just connected to you!".format(user = self_user)
    conn.send(greeting_msg.encode('utf-8'))

    unsent_msgs = get_unsent_messages(target_name)
    if len(unsent_msgs) != 0:
        conn.send("Offline message from {user}\n".format(user=self_user).encode('utf-8'))
        for msg in unsent_msgs:
            message = msg[3]
            conn.send(message.encode('utf-8'))
            delete_sent_message(msg[0], msg[1], msg[2], msg[3])
            insert_message_send(self_user, target_name, message, True)
    while True:
        if discovery_module.checkUserStatus(target_name) == "offline":
            print(
                "{user} is offline right now. You are in offline sending mode. You can enter messages and they will be sent once the user is online, or type 'exit' to talk to another user.".format(user=target_name))
            msg = input("msg: ")
            while msg != "exit":
                insert_message_send(self_user, target_name, msg, False)
                msg = input("msg: ")
            conn.close()
            return
        else:
            target_user_host = discovery.getAllUsers()[target_name]["ip_address"]
            target_user_port = discovery.getAllUsers()[target_name]['port']
            if (target_user_host != original_host) or (target_user_port != original_port):
                conn = connect_socket(target_user_host, target_user_port)
            message = input()
            conn.send(message.encode('utf-8'))
            insert_message_send(self_user, target_name, message, True)

def connect_socket(HOST, PORT):
    # create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the server
    client_socket.connect((TARGET_HOST, TARGET_PORT))

    return client_socket

# start two threads to receive and send messages
# receive_thread = threading.Thread(target=receive)
# receive_thread.start()

if __name__ == "__main__":
    try:
        username = input("Enter your username (Your username must be the same as your username used in the Receiver): ")
        discovery_api_host = input("Enter discovery_api server's host: ")
        discovery_api_port = input("Enter discovery_api server's port: ")
        discovery = Discovery(discovery_api_host, discovery_api_port)
        TARGET_HOST = None
        TARGET_PORT = None
        while True:
            users = discovery.getAllUsers()
            print("users: ")
            for user in users:
                if user != username:
                    print("\t"+user+": "+ str(users[user]))
            # print(users)
            target_user = input("Enter the username that you want to talk to: ")
            if target_user not in users:
                print("User does not exists, please enter a valid username that exists in the users: ")
            else:
                TARGET_HOST = users[target_user]["ip_address"]
                TARGET_PORT = users[target_user]['port']
                break
        # TARGET_HOST = input("Enter target host: ")
        # TARGET_PORT = int(input("Enter target port: "))

        if discovery.checkUserStatus(target_user) == "offline":
            print("{user} is offline right now. You are in offline sending mode. You can enter messages and they will be sent once the user is online, or type 'exit' to talk to another user.".format(user = target_user))
            msg = input("msg: ")
            while msg != "exit":
                insert_message_send(username, target_user, msg, False)
                msg = input("msg: ")
        else:
            sock = connect_socket(TARGET_HOST, TARGET_PORT)
            send_thread = threading.Thread(target=send, args=(discovery, username, target_user, TARGET_HOST, TARGET_PORT, sock))
            send_thread.start()
    except Exception as e:
        print("Exception msg: "+ str(e))
        sys.exit(0)
