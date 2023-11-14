import mysql.connector
from hashlib import sha256

class User:
    def __init__(self, id, username, password, is_admin):
        self.id = id
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def __str__(self):
        return f"User(id={self.id}, username={self.username}, password={self.password}, is_admin={self.is_admin})"

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()
        self.createTables()

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor
    
    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def createTables(self):
        self.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, is_admin BOOLEAN NOT NULL DEFAULT FALSE)")
        self.commit()

    def insertUser(self, username, password, is_admin=False):
        hashedPass = sha256(password.encode()).hexdigest()
        self.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)", (username, hashedPass, is_admin))
        self.commit()

    def loginUser(self, username, password):
        hashedPass = sha256(password.encode()).hexdigest()
        self.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hashedPass))
        user = self.cursor.fetchone()
        if user is None:
            return None
        return User(*user)
    
    def getUser(self, username):
        self.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = self.cursor.fetchone()
        if user is None:
            return None
        return User(*user)
    
    def checkIfExist(self, username):
        self.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = self.cursor.fetchone()
        if user is None:
            return False
        return True

    
