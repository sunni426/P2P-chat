import sqlite3
import logging
from datetime import datetime

logging.basicConfig(filename='database.log', 
                    filemode='w',
                    level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s: %(message)s')

def connect():
    conn = sqlite3.connect('chats.db')
    cursor = conn.cursor()
    logging.info("Connected to database successfully")

    return conn, cursor

def create_table():
    conn, cursor = connect()
    query = "CREATE TABLE IF NOT EXISTS CHATS (DATE_TIME TEXT NOT NULL, SENDER TEXT NOT NULL, RECEIVER TEXT NOT NULL, MESSAGE_CONTENT TEXT NOT NULL, MESSAGE_SENT INTEGER);"
    cursor.execute(query)
    conn.commit()

    logging.info("Chats table created successfully")

def insert_message_send(sender: str, receiver: str, message: str, is_sent: bool):
    date_time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    is_sent_int = int(is_sent == True)

    conn, cursor = connect()
    query = "INSERT INTO CHATS VALUES (?, ?, ?, ?, ?);"
    val = (date_time_now, sender, receiver, message, is_sent_int)
    cursor.execute(query, val)
    conn.commit()

    logging.info("New Message: %s, %s, %s, sent: %s inserted successfully", date_time_now, sender, 
                 receiver, str(is_sent))
    

def insert_message_received(sender: str, receiver: str, message: str):
    date_time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    conn, cursor = connect()
    query = "INSERT INTO CHATS (DATE_TIME, SENDER, RECEIVER, MESSAGE_CONTENT) VALUES (?, ?, ?, ?);"
    val = (date_time_now, sender, receiver, message,)
    cursor.execute(query, val)
    conn.commit()

    logging.info("New Message: %s, %s, %s, received inserted successfully", date_time_now, sender, receiver)
    

def get_chat_messages(username: str):
    conn, cursor = connect()
    query = "SELECT * FROM CHATS WHERE SENDER = ? OR RECEIVER = ?;"
    val = (username, username,)
    cursor.execute(query, val)
    result = cursor.fetchall()

    return result


def get_unsent_messages(receiver: str):
    conn, cursor = connect()
    query = "SELECT * FROM CHATS WHERE RECEIVER = ? AND MESSAGE_SENT = 0;"
    val = (receiver,)
    cursor.execute(query, val)
    result = cursor.fetchall()

    return result


create_table()
# insert_message_send("sarah", "sunni", "hello!", True)
# insert_message_send("sarah", "sam", "hi!", False)
# insert_message_received("sunni", "sarah", "Hi Sarah!")
# print(get_chat_messages("sunni"))
# print()
# print(get_chat_messages("sam"))
# print()
# print(get_unsent_messages("sunni"))
# print()
# print(get_unsent_messages("sam"))