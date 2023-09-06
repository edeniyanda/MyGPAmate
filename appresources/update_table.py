import sqlite3

class update_table:
    def __init__(self, path_to_database:str, table_name:str, level:str, semester:str) -> None:
        self.level = level
        self.semester = semester
        self.path_to_database = path_to_database
        self.table_name = table_name
    def load_course_from_database(self) -> tuple:
        self.conn = sqlite3.connect(self.path_to_database)
        self.cur = self.conn.cursor()
        
        query = f"SELECT * FROM '{self.table_name}'"
        
        self.cur.execute(query)
        
        self.courses_info = self.cur.fetchall() 
        
        return self.courses_info
    
    def save_courses_to_database(self, course_data:list) -> None:
        self.conn = sqlite3.connect(self.path_to_database)
        self.cur = self.conn.cursor()
        
        self.cur.execute(f"DELETE FROM '{self.table_name}'")
        
        self.conn.commit()
        
        for data in course_data:
            query = f"INSERT INTO '{self.table_name}' (course_title, course_code, course_unit) VALUES (?,?,?)"
            self.cur.execute(query, data)
            self.conn.commit()
                     
        self.conn.close()