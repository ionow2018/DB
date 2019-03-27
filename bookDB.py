import sqlite3


class DB:
    def __init__(self):
        conn = sqlite3.connect('books.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class UsersModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(64),
                             password_hash VARCHAR(64),
                             lock INTEGER,
                             email VARCHAR(64),
                             level INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, email, password_hash):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, email, password_hash, lock, level) 
                          VALUES (?,?,?,0,3)''', (user_name, email, password_hash))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = " + str(user_id))
        row = cursor.fetchone()
        return row

    def lock(self, user_id, lock=1):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET lock = ? WHERE id = ?", (lock, user_id))

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users ORDER BY level, user_name")
        rows = cursor.fetchall()
        return rows

    def delete(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE id = ?''' + str(user_id))
        cursor.close()
        self.connection.commit()

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row) if row else (False,)

    def existUser(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?",
                       user_name)
        row = cursor.fetchone()
        return True if row else False


class BooksModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(64),
                             author VARCHAR(64),
                             genre VARCHAR(16),
                             description VARCHAR(256),
                             part VARCHAR(512),
                             link VARCHAR(128),
                             user_id INTEGER,
                             date DATETIME)''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, author, genre, description, part, link, user_id, date):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO books 
                          (title, author, genre, description, part, link, user_id, date) 
                          VALUES (?,?,?,?,?,?,?,?)''',
                       (title, author, genre, description, part, link, user_id, date))
        cursor.close()
        self.connection.commit()

    def update(self, title, author, genre, description, part, link, user_id, date, id):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE books SET title=?, author=?, genre=?, description=?, part=?,
                        link=?, user_id=?, date=? WHERE id=?''',
                       (title, author, genre, description, part, link, user_id, date, id))
        cursor.close()
        self.connection.commit()

    def update_link(self, link, id):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE books SET link=? WHERE id=?''', (link, id))
        cursor.close()
        self.connection.commit()

    def get(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM books WHERE id = ''' + str(id))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books ORDER BY author")
        rows = cursor.fetchall()
        return rows

    def exist_book(self, title, author):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books WHERE title = ? AND author = ?",
                       (title, author))
        row = cursor.fetchone()
        return True if row else False

    def delete(self, id):
        cursor = self.connection.cursor()
        # print(id)
        cursor.execute('''DELETE FROM books WHERE id = ''' + str(id))
        cursor.close()
        self.connection.commit()


class JournalsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS journals 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             date DATETIME,
                             user_id INTEGER,
                             action_id INTEGER,
                             object_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, date, user_id, action_id, object_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO journals 
                          (date, user_id, action_id, object_id) 
                          VALUES (?,?,?,?)''',
                       (date, user_id, action_id, object_id))
        cursor.close()
        self.connection.commit()

    def get(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM journals WHERE id = ?" + str(id))
        row = cursor.fetchone()
        return row


    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM journals")
        rows = cursor.fetchall()
        return rows


# db = DB()
# users = UsersModel(db.get_connection())
# users.init_table()
# books = BooksModel(db.get_connection())
# books.init_table()
# books.add_author()
