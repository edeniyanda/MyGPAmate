import sqlite3


class load_data_from_db:
    def __init__(self, path_database:str, table:str) -> None:
        self.path_database = path_database
        self.table = table
        
    def load_data(self) -> tuple:
        self.conn = sqlite3.connect(self.path_database)
        self.cur = self.conn.cursor()

        # Retrieve settings from the database
        select_query = f"SELECT * FROM {self.table}"
        self.cur.execute(select_query)
        self.data = self.cur.fetchone()  
        
        self.conn.close()
        return self.data
