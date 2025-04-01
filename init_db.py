import sqlite3

# Подключение к базе (если нет — создастся автоматически)
conn = sqlite3.connect("vacancies.db")
cursor = conn.cursor()

# Создание таблицы, если её нет
cursor.execute('''
CREATE TABLE IF NOT EXISTS vacancies (
    id INTEGER PRIMARY KEY,
    vacancy_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    schedule TEXT,
    employment TEXT,
    city TEXT,
    experience TEXT,
    salary TEXT
);
''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("База данных vacancies.db успешно создана!")
