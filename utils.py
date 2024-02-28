from typing import Any
from config import config
import requests
import psycopg2


def get_employers_data(api_key: str, employers_ids: list[str]) -> list[dict[str, Any]]:
    '''Получение информации о работодателях по API'''
    employer_data = []
    for emp_id in employers_ids:
        api_call = requests.get(f'{api_key}/{emp_id}').json()
        employer_data.append([
                {'id': api_call['id']},
                {'company_name': api_call['name']},
                {'url': api_call['alternate_url']},
                {'vacancies_qty': api_call['open_vacancies']},
                {'description': api_call['description']}
        ])
    return employer_data


def get_vacancy_data(api_key, employer_ids: list[int], ) -> list[dict[str, Any]]:
    '''Получение вакансий конкретного работодателя'''
    vacancy_data = []
    for id in employer_ids:
        api_call = requests.get(api_key, {'employer_id': int(id)}).json()['items']
        for vac in api_call:
            salary = vac['salary'] if vac['salary'] else None
            from_salary = salary['from'] if salary else None
            to_salary = salary['to'] if salary else None
            currency = salary['currency'] if salary else None
            vacancy_data.append([
                {'employer_id': vac['employer']['id']},
                {'vacancy_id': vac['id']},
                {'vacancy_name': vac['name']},
                {'from_salary': from_salary},
                {'to_salary': to_salary},
                {'currency': currency},
                {'country': vac['area']['name']},
                {'url': vac['alternate_url']},
                {'experience': vac['experience']['name']},
                {'requirement': vac['snippet']['requirement']}
            ])
    return vacancy_data


def create_database(database_name: str, params: dict) -> None:
    '''Создание базы данных и таблиц для сохранения данных'''
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            try:
                cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
                cur.execute(f"CREATE DATABASE {database_name}")
            except Exception:
                pass
    finally:
        conn.close()

    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                    cur.execute('DROP TABLE employers CASCADE')
    except Exception:
        pass

    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE employers(
                id INT PRIMARY KEY,
                company_name VARCHAR(50),
                url VARCHAR(70),
                vacancies_qty SMALLINT,
                description TEXT
            )
            ''')

    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute('DROP TABLE vacancies CASCADE')
    except Exception:
        pass

    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE vacancies(
                employer_id INT REFERENCES employers(id),
                vacancy_id INT PRIMARY KEY,
                vacancy_name VARCHAR(100),
                from_salary INT,
                to_salary INT,
                currency VARCHAR(3),
                country VARCHAR(30),
                url VARCHAR(100),
                experience VARCHAR(20),
                requirement TEXT
            )
            ''')


def save_employers_to_database(emp_list: list[dict[str, Any]], database_name: str, params: dict) -> None:
    '''Сохранение данных в базу'''
    conn=psycopg2.connect(**params)
    with conn.cursor() as cur:
        cur.execute('TRUNCATE TABLE employers CASCADE')
        for employer in emp_list:
            cur.execute(f'''
            INSERT INTO employers (id, company_name, url, vacancies_qty, description) VALUES
            (%s, %s, %s, %s, %s)''',
            (employer[0]['id'],
             employer[1]['company_name'],
             employer[2]['url'],
             employer[3]['vacancies_qty'],
             employer[4]['description']))
    conn.commit()


def save_vacancies_to_database(vac_list: list[dict[str, Any]], database_name: str, params: dict) -> None:
    '''Сохранение данных в базу'''
    conn=psycopg2.connect(**params)
    with conn.cursor() as cur:
        cur.execute('TRUNCATE TABLE vacancies CASCADE')
        for vacancy in vac_list:
            cur.execute(f'''
            INSERT INTO vacancies (employer_id, vacancy_id, vacancy_name, from_salary, to_salary, currency, country, url,experience, requirement)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
            (vacancy[0]['employer_id'],
             vacancy[1]['vacancy_id'],
             vacancy[2]['vacancy_name'],
             vacancy[3]['from_salary'],
             vacancy[4]['to_salary'],
             vacancy[5]['currency'],
             vacancy[6]['country'],
             vacancy[7]['url'],
             vacancy[8]['experience'],
             vacancy[9]['requirement']))
    conn.commit()
