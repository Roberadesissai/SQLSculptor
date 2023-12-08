import sqlite3


class SQLSculptor:
    def __init__(self):
        self.conn = sqlite3.connect("lite.db")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS store (item TEXT, quantity INTEGER, price REAL)")
        self.conn.commit()

    def insert(self, item, quantity, price):
        self.cur.execute("INSERT INTO store VALUES (?, ?, ?)", (item, quantity, price))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM store")
        rows = self.cur.fetchall()
        return rows

    def delete(self, item):
        self.cur.execute("DELETE FROM store WHERE item=?", (item,))
        self.conn.commit()

    def update(self, quantity, price, item):
        self.cur.execute("UPDATE store SET quantity=?, price=? WHERE item=?", (quantity, price, item))
        self.conn.commit()

    def __del__(self):
        self.conn.close()



if __name__ == "__main__":
    sculptor = SQLSculptor()