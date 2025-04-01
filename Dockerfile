# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Команда для создания базы данных
RUN python database.py

# Создаём базу данных перед запуском
RUN python init_db.py

# Команда для запуска бота
CMD ["python", "bot.py"]
