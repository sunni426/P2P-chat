import requests


class Discovery:

    '''
    api_host: it must be the same as the host running the discovery_api.py module
    api_port: it must be the same as the port running the discovery_api.py module
    '''
    def __init__(self, api_host, api_port):
        self.host = api_host
        self.port = api_port
        self.BASE_URL = "http://"+self.host+":"+str(self.port)


    '''
    What it does:
        It gets all the users, either offline or online, from the discovery database
    Why use it:
        User wants to find someone to chat, so they call this function to get all other
        users information, and choose one to talk to
    Note:
        The return is a dictionary, format:
        {'sam': 
            {'username': 'sam', 'status': 'online', 'ip_address': '127.0.0.1', 'port': 1234}
        }
    '''
    def getAllUsers(self):
        url = self.BASE_URL+"/discover/get_all_users"
        response = requests.get(url)
        return response.json()


    '''
    Why use it:
        To create a database if there is no database for discovery module.
        This normally happens when people first use the discovery_api.py and discovery.
    '''
    def createDatabase(self):
        url = self.BASE_URL + "/discover/create_table/"

        response = requests.post(url)
        return response.json()["message"]


    '''
    By given a  username, status(online/offline), ip, and port, this function will insert the
    user into the database
    '''
    def insertUser(self, username, status, ip, port):
        url = self.BASE_URL+"/discover/insert_user/"

        data = {
            "username": username,
            "status": status,
            "ip": ip,
            "port": port
        }

        response = requests.post(url, json=data)

        return response.json()["message"]  # Print the response body as JSON

    '''
    What it does:
        Given a user, it updates the user's ip and port in the database, and make his status
        to 'online'
    Why use this function:
        When a user start using the p2p app, they need to make sure their ip and port is correct
        so other people can check out their ip and port and establish connection with them
    Note:
        user needs to make sure their username is correct, and make sure they are in the db. The
        API doesn't check
    '''
    def updateIpAndPort(self, username, ip, port):
        url = self.BASE_URL+"/discover/update_ip_and_port/"

        data = {
            "username": username,
            "ip_address": ip,
            "port": port
            }

        response = requests.post(url, json=data)

        return response.json()["message"]

    '''
    What it does:
        Given a username, this function will update the user's status to 'offline' in database.
    Why it exists:
        Before a user closes the p2p chat, the p2p app should call this function to mark this 
        user as offline in the database
    NOTE: 
        User is responsible for entering their correct names. The API will not check if 
        such user exists
    '''
    def setUserOffline(self, username):
        url = self.BASE_URL + "/discover/set_offline_status/"

        data = {"username": username}

        response = requests.post(url, json=data)

        return response.json()["message"]


if __name__ == "__main__":
    d = Discovery("127.0.0.1", 8000)
    print(d.getAllUsers())
    print(d.createDatabase())
    # print(d.insertUser("locale", "online", "127.0.0.1", 1987))
    # print(d.updateIpAndPort("locale", "198.12.2.3", 1234))
    # print(d.setUserOffline("locale"))
    # print(d.setUserOffline("nobody"))

