import requests
import logging
import sqlite3

logging.basicConfig(level=logging.INFO)


def get_db():
    return sqlite3.connect('vacancies.db')


def parse_vacancies(text, salary, employment, experience):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': text,
        'area': '1',  # Москва
        'salary': salary,
        'employment': employment,
        'experience': experience,
        'per_page': 20,
        'page': 0
    }
    response = requests.get(url, params=params)
    vacancies = response.json().get('items', [])
    print(vacancies)
    # return

    result = []
    for vacancy in vacancies:
        vacancy_id = vacancy['id']
        name = vacancy['name']
        url = vacancy['url']
        #  График
        schedule = vacancy.get('schedule', {}).get('name', 'Отсутствует')
        #  Занятость
        employment = vacancy.get('employment', {}).get('name', 'Отсутствует')
        city = vacancy['area']['name']
        experience = vacancy.get('experience', {}).get('name', 'Отсутствует')

        salary = vacancy['salary']

        if salary is not None:
            if salary['from'] is None:
                salary['from'] = '_'
            if salary['to'] is None:
                salary['to'] = '_'
            salary = f"{salary['from']}-{salary['to']} {salary['currency']}"
        else:
            salary = 'Отсутствует'
        
        result.append((vacancy_id, name, schedule, employment, city, experience, salary))

    return result

# Функция для сохранения данных в базу данных
def save_data_to_db(data):
    db = get_db()
    cursor = db.cursor()
    for item in data:
        cursor.execute(
            "INSERT INTO vacancies (vacancy_id, name, schedule, employment, city, experience, salary) VALUES (?, ?, ?, ?, ?, ?, ?)",
            item
        )
    db.commit()
    cursor.close()
    db.close()

if __name__ == '__main__':
    data = parse_vacancies()
    save_data_to_db(data)
    logging.info('Data successfully parsed and saved to the database.')