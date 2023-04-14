# p2p-chat

## Functionality
1) discovery_server.py: maintains list of sockets, currrently echoes all messages sent/received among all client users
2) client.py: init

## Limitations
- currently only supports 2 users with hardcoded IP addresses & port numbers

# To Do:
1) update on/offline socket status in socket_list in discovery_server
    & other discovery server implementations
2) take port number (and IP Address?) as command-line arguments (change hardcoded IP address stuff)
3) incorporate database & offline caching of messages (0/1 check)