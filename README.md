# Demo:
### You can follow the step from the demo to implement the p2p chat or read the step starting from the 'Instruction' below <br />
### Link: https://drive.google.com/file/d/1LZ_ODt23Hg8_MYUfkt_df-6CL_sNSe3x/view?usp=share_link 

# File explanation:
### Receiver.py: 
The code that allow other users to connect to receive messages sent from those connected users
### Sender.py: 
The code that allow a user connect to a specific user, and then send messages to that user. 
#### So a user will need 2 windows, one runs Receiver.py, to receive messages from other users, and one runs Sender.py, to send message to the a user this user connects to
### sqlite3_database.py: 
A module that creates a local database and store messages. Sender.py use this module to insert sent and unsent message. The database is to store all the message a current user wants to send, and for the messages current user wants to send to a target user that is offline, they will be stored in the local database first. When the target user is online, and the current user is online, current user will automatically send those message to that target user before sending any message.
### discover_api.py: 
This is the discover module that has all the endpoints to manage the users. This is a FastAPI that we wrote.
### discovery.py: 
This is the python code that our Receiver.py and Sender.py use to interact with the discover_api.py FastAPI. Because FastAPI is not like class and function, so we create the discovery.py to have a class, so we can use the python code to interact with the API

# NOTE:
## The p2p chat currently only support local host chatting, i.e. host = 127.0.0.1
## For communication, 2 users connect to each other by connecting them with their host and port, a middle server is not used. During the demo, when I enter message, the discover server's API is called. This is because I am calling to the discover server to check if the any of them is still online. It is not used as a messenger to pass messages between 2 users.

# Instruction
# To start:
1. clone this repository
2. Go into the p2p-chat folder from terminal: cd p2p-chat

# Fist, start up the discover server by running the following commands:
  1. uvicorn discover_api:app --reload

# Create first user 'Sam' by running the following command 
## Open a new terminal
## Commands
1. python3 Receiver.py
2. Enter '127.0.0.1' when prompted "Enter discovery_api server's host:"
3. Enter '8000' when prompted "Enter discovery_api server's port:"
4. Enter 'Sam' when prompted "Enter your username:" <br />
It will say "You don't exists in the database. Now we are creating a new account for you.", because you are running this program the first time, and the database doesn't have any user, including "Sam"
6. Enter '127.0.0.1' when prompted "Enter your host:"
7. Enter '4444' or a port number you like when prompted "Enter your port:"
8. Now you are online, and you can be connected by other users.

# Create second user 'Carol' by running the following command
## Open a new terminal
## Commands:
1. python3 Receiver.py
2. Enter '127.0.0.1' when prompted "Enter discovery_api server's host:"
3. Enter '8000' when prompted "Enter discovery_api server's port:"
4. Enter 'Carol' when prompted "Enter your username:" <br />
It will say "You don't exists in the database. Now we are creating a new account for you.", because Carol is a new user, and it doesn't exist in the database
6. Enter '127.0.0.1' when prompted "Enter your host:"
7. Enter '5555' or a port number you like when prompted "Enter your port:", just make sure it's a different one than Sam's port
8. Now you are online, and you can be connected by other users.


# Create a window for Sam to talk to Carol by running the following command:
## Open a new terminal
## Commands
1. python3 Sender.py
2. Enter "Sam" when prompted "Enter your username (Your username must be the same as your username used in the Receiver): " <br /> 
NOTE: Make sure the name is the same as you created for the Sam receiver
3. Enter '127.0.0.1' when prompted: "Enter discovery_api server's host:"
4. Enter '8000' when prompted: "Enter discovery_api server's port:" <br />
Now the discover server will display you the users that you can talk to, both online and offline. You will see the following message: <br />
users: <br/>
	Carol: {'username': 'Carol', 'status': 'online', 'ip_address': '127.0.0.1', 'port': 5555}

6. Enter 'Carol' when prompted: "Enter the username that you want to talk to:"
7. Now your sender window is connected to Carol, and Carol's Receiver window will display "Sam just connected to you!"
8. You can enter any thing press enter key to send messages

# Create a window for Carol to talk to Sam by running the following command:
## Open a new terminal
## Commands
1. python3 Sender.py
2. Enter "Carol" when prompted "Enter your username (Your username must be the same as your username used in the Receiver): " <br /> 
NOTE: Make sure the name is the same as you created for the Carol receiver
3. Enter '127.0.0.1' when prompted: "Enter discovery_api server's host:"
4. Enter '8000' when prompted: "Enter discovery_api server's port:" <br />
Now the discover server will display you the users that you can talk to, both online and offline. You will see the following message: <br />
users: <br/>
	Sam: {'username': 'Sam', 'status': 'online', 'ip_address': '127.0.0.1', 'port': 5555}

6. Enter 'Sam' when prompted: "Enter the username that you want to talk to:"
7. Now your sender window is connected to Sam, and Sam's Receiver window will display "Carol just connected to you!"
8. You can enter any thing press enter key to send messages

# Current situation:
Now, Sam has two window, one is runs Receiver.py, one runs Sender.py. The Receiver is to display messages sent from users that connect to Sam, and the Sender is for Sam to send message to the user Sam connects to <br />
Carol has the same things, one window runs Receiver.py, one runs Sender.py. The Receiver is to display message sent from users that connect to Carol, and the Sender is for Carol to send message to the user Carol connects to <br />

Right now, Sam can type things in the window that runs his Sender.py and send them, then the message will display in Carol's window that runs Receiver.py <br />
Also, Carol can type things in the window that runs her Sender.py and send them, then the message will display in Sam's window that runs Receiver.py <br />

# To test offline message sending
## Step 1
1. press 'control c' in Carol's Receiver window, to use KeyboardInterrupt to stop Carol's programs, to simulate she's offline. Don't close Carol's Receiver window
2. In Sam's sender window, if you type something, it will display: <br />
"Carol is offline right now. You are in offline sending mode. You can enter messages and they will be sent once the user is online, or type 'exit' to talk to another user."  
3. Enter anything you want when prompted: "msg: "
4. Enter 'exit' when prompted: "msg: " to exit offline sending mode <br />
Now Sam's sender window program is terminated. Run the following command lines to bring back Sam's sender program:
5. Don't close the window
## Step 2: bring Carol back online
### In Carol's receiver windw where we did the Step 1.1, run the following command
1. python3 Receiver.py
2. Enter '127.0.0.1' when prompted: "Enter discovery_api server's host: "
3. Enter '8000' when prompted: "Enter discovery_api server's port: "
4. Enter "Carol" when prompted: "Enter your username: "
5. Enter "127.0.0.1" when prompted: "Enter your host: "
6. Enter "5555" or the any port you want when prompted: "Enter your port: ". Just make sure the port is not the same as Sam's port
7. It will display "You are online. Waiting for other users to connect to you..."

## Step 3: bring back Sam's sender window, and connect to Carol. Once Sam's sender window connects to Carol's window, all the messages that was typed in Step 1.3 will be sent to Carol, and you are not even typing.
### In Sam's sender window, run the following command
1. python3 Sender.py
2. Enter 'Sam' when prompted: "Enter your username (Your username must be the same as your username used in the Receiver):"
3. Enter '127.0.0.1' when prompted: "Enter discovery_api server's host:"
4. Enter '8000' when prompted: "Enter discovery_api server's port:" <br />
It will display: <br />
users: 
	Carol: {'username': 'Carol', 'status': 'online', 'ip_address': '127.0.0.1', 'port': 5555}
6. Enter 'Carol' when prompted: "Enter the username that you want to talk to: "
7. In Carol's receiver window we created in Step 2, it will display: <br />
Sam just connected to you! <br />
Offline message from Sam <br />
messages...

