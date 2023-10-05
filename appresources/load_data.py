import sqlite3


class load_data_from_db:
    def __init__(self, path_database:str, table:str, save_data:tuple=None) -> None:
        self.path_database = path_database
        self.table = table
        self.save_data = save_data
        
    def load_data(self) -> tuple:
        self.conn = sqlite3.connect(self.path_database)
        self.cur = self.conn.cursor()

        # Retrieve settings from the database
        select_query = f"SELECT * FROM {self.table}"
        self.cur.execute(select_query)
        self.data = self.cur.fetchone()  
        
        self.conn.close()
        return self.data
    
    def load_data_for_grade(self) -> tuple:
        self.conn = sqlite3.connect(self.path_database)
        self.cur = self.conn.cursor()

        # Retrieve settings from the database
        select_query = f"SELECT * FROM {self.table}"
        self.cur.execute(select_query)
        self.data = self.cur.fetchall()  
        
        self.conn.close()
        return self.data
    
    def save_data_to_grader(self):
        self.conn = sqlite3.connect(self.path_database)
        self.cur = self.conn.cursor()
        
        self.cur.execute(f"DELETE FROM {self.table}")
        self.conn.commit()
        
        for i in range(len(self.save_data)):
            query = f"INSERT INTO '{self.table}' (grade, unit) VALUES (?,?)"
            self.cur.execute(query, self.save_data[i])
            self.conn.commit()
        self.conn.close()
        
        
    
