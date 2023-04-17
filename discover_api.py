import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

# Connect to database

app = FastAPI()

database_str = 'discover.db'


class InsertUserItem(BaseModel):
    username: str
    status: str
    ip: str
    port: int


class SetOfflineStatusItem(BaseModel):
    username: str


class DeleteItem(BaseModel):
    username: str


class UpdateIpAndPortItem(BaseModel):
    username: str
    ip_address: str
    port: int


class CheckUserExistsItem(BaseModel):
    username: str


def connectToDatabase():
    conn = sqlite3.connect(database_str)
    return conn


# Create a table
@app.post("/discover/create_table/")
def createTable():
    try:
        conn = connectToDatabase()
        conn.execute('''CREATE TABLE IF NOT EXISTS users
                     (username VARCHAR(100) PRIMARY KEY,
                      status VARCHAR(10) NOT NULL,
                      ip_address VARCHAR(20) NOT NULL,
                      port INTEGER NOT NULL);''')
        conn.commit()
        conn.close()
        return {"message":"success"}
    except Exception as e:
        return {"message": str(e)}


# Insert data
@app.post("/discover/insert_user/")
def insertUser(item: InsertUserItem):
    createTable()
    try:
        conn = connectToDatabase()
        username = item.username
        status = item.status
        ip = item.ip
        port = item.port
        cursor = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row is not None:
            print("Username {name} already exists.".format(name=username))
            return {"message":"user already exists"}
        else:
            conn.execute("INSERT INTO users (username, status, ip_address, port) VALUES (?, ?, ?, ?)",
                         (username, status, ip, port))
            conn.commit()
            conn.close()
            return {"message":"success"}
    except Exception as e:
        return {"message": str(e)}


@app.get("/discover/get_all_users")
# Query data
def getAllUsers():
    try:
        createTable()
        conn = connectToDatabase()
        dic = {}
        cursor = conn.execute("SELECT * from users")
        for row in cursor:
            username = row[0]
            status = row[1]
            ip_address = row[2]
            port = row[3]
            dic[username] = {'username': username, 'status': status, 'ip_address': ip_address, 'port': port}
        conn.close()
        return dic
    except Exception as e:
        return {"message": str(e)}


@app.get("/discover/check_user_exists/{username}")
def checkUserExists(username):
    try:
        createTable()
        conn = connectToDatabase()
        cursor = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            return {"message": "exists"}
        else:
            return {"message": "not exists"}
    except Exception as e:
        return {"message": str(e)}

@app.get("/discover/check_status/{username}")
def checkUserStatus(username):
    try:
        createTable()
        conn = connectToDatabase()
        cursor = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            print(row)
            return {"message": row[1]}
        else:
            print("username not exists")
            return {"message": "user not exists"}
    except Exception as e:
        return {"message": str(e)}



@app.post("/discover/set_offline_status/")
# Update data
def setOfflineStatus(item: SetOfflineStatusItem):
    try:
        createTable()
        username = item.username
        conn = connectToDatabase()
        conn.execute("UPDATE users SET status = ? WHERE username = ?", ("offline", username))
        conn.commit()
        conn.close()
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}


@app.post("/discover/update_ip_and_port/")
def updateIpAndPort(item: UpdateIpAndPortItem):
    try:
        createTable()
        conn = connectToDatabase()
        username = item.username
        ip_address = item.ip_address
        port = item.port
        conn.execute("UPDATE users SET status = ?, ip_address = ?, port = ? WHERE username = ?",
                     ("online", ip_address, port, username))
        conn.commit()
        conn.close()
        return {"message":"success"}
    except Exception as e:
        return {"message": str(e)}


# Delete data
@app.post("/discover/delete_user/")
def deleteUser(item: DeleteItem):
    try:
        createTable()
        conn = connectToDatabase()
        username = item.username
        conn.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}

