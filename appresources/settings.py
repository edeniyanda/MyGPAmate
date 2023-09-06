import sqlite3

class settings:
    def __init__(self, path_database:str, table:str="app_settings"):
        self.path_database = path_database
        self.table = table
    def load_data(self) -> tuple:
        self.conn = sqlite3.connect(self.path_database)
        self.cur = self.conn.cursor()

        # Retrieve settings from the database
        select_query = f"SELECT * FROM {self.table} WHERE id = ?"
        row_id = 1  # The ID of the row
        self.cur.execute(select_query, (row_id,))
        self.data = self.cur.fetchone()  
        
        self.conn.close()
        return self.data
    
    def save_settings(self, data:tuple) -> None:
        self.conn = sqlite3.connect(self.path_database)
        self.cur = self.conn.cursor()
        
        # Clear all saved settings
        self.cur.execute(f"DELETE FROM {self.table}")
        self.conn.commit()
        
        # Insert all new settings
        query = f"INSERT INTO {self.table} (id, theme, font_size, font_type, current_level, current_semester) VALUES (?,?,?,?,?,?)"
        
        self.cur.execute(query, data)
        
        self.conn.commit()
        self.conn.close()
        