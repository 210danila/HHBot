import sqlite3

conn = sqlite3.connect('vacancies.db')

cursor = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS vacancies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vacancy_id INTEGER,
    name TEXT,
    schedule TEXT,
    employment TEXT,
    city TEXT,
    experience TEXT,
    salary TEXT
);
"""

cursor.execute(create_table_query)

conn.commit()
conn.close()

print("Table created successfully.")
