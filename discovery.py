import requests


class Discovery:
    def __init__(self, api_host, api_port):
        self.host = api_host
        self.port = api_port
        self.BASE_URL = "http://"+self.host+":"+str(self.port)

    def getAllUsers(self):
        url = self.BASE_URL+"/discover/get_all_users"
        response = requests.get(url)
        return response.json()

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

    def updateIpAndPort(self, username, ip, port):
        url = self.BASE_URL+"/discover/update_ip_and_port/"

        data = {
            "username": username,
            "ip_address": ip,
            "port": port
            }

        response = requests.post(url, json=data)

        return response.json()["message"]

    def setUserOffline(self, username):
        url = self.BASE_URL + "/discover/set_offline_status/"

        data = {"username": username}

        response = requests.post(url, json=data)

        return response.json()["message"]


    def checkUserExists(self, username):
        url = self.BASE_URL + "/discover/check_user_exists/"+username
        response = requests.get(url)
        if response.json()['message'] == "exists":
            return True
        else:
            return False

    def checkUserStatus(self, username):
        url = self.BASE_URL + "/discover/check_status/"+username
        response = requests.get(url)
        if response.json()['message'] == "user not exists":
            return None
        else:
            return response.json()['message']

if __name__ == "__main__":
    d = Discovery("127.0.0.1", 8000)
    # d.getAllUsers()
    # print(d.checkUserExists("sam"))
    # print(d.checkUserExists("samy"))
    print(d.checkUserStatus("sam"))
    print(d.checkUserStatus("sammy"))
    print(d.checkUserStatus("lianghuanjia"))
    # print(d.updateIpAndPort("locale", "198.12.2.3", 1234))
    # print(d.setUserOffline("locale"))
    # print(d.setUserOffline("nobody"))

