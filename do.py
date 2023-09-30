import sqlite3

# Replace 'your_database.db' with the name of your SQLite database
db_file = 'mygpamatedata.db'
new_column_name = 'grade'
data_type = 'INTEGER'

# List of table names to update
tables_to_update = [ '300FirstSemester', '300SecondSemester', '400FirstSemester', '400SecondSemester']

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Loop through each table and add the new column
for table_name in tables_to_update:
    alter_query = f"ALTER TABLE '{table_name}' ADD COLUMN {new_column_name} {data_type}"
    cursor.execute(alter_query)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Successful")
