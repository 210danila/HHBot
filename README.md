# HHBot - бот для поиска вакансий

Скрипт позволяет искать вакансии на hh.ru через телеграмм бота.
Стек: python, aiogram, sqlite3, docker

## Установка:

#### Установка докер и docker-compose:
https://techno-tim.github.io/posts/docker-compose-install/

#### Создаем виртуальную среду, устанавливаем зависимости:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

#### Создаем файл .env и записываем в него токен нашего бота:
touch .env
API_TOKEN=YOUR_TOKEN

#### Собираем докер контейнер и запускаем в фоновом режиме:
sudo docker compose up --build -d

 ✔ bot                     Built
 ✔ Container telegram_bot  Started

#### Проверяем что контейнер работает:
sudo docker ps

#### Если есть ошибки или бот не работает, можем это проверить через лог:
sudo docker logs -f telegram_bot
