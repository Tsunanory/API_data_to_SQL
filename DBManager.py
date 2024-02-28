import psycopg2
from config import config


# print(requests.get(key, {'per_page':100}).json())
# print(requests.get(f'{key_emp}/{3529}',{'per_page':20}).json())


class DBManager:
    credentials = config()


    def get_companies_and_vacancies_count(self):
        '''Получение списка всех компаний с количеством открытых вакансий в каждой'''
        with psycopg2.connect(**self.credentials) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT company_name, vacancies_qty FROM employers')
                results = cur.fetchall()
                return '\n'.join(str(result) for result in results)

    def get_all_vacancies(self):
        '''получение списка всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию'''
        with psycopg2.connect(**self.credentials) as conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT company_name, vacancies.vacancy_name, 
                            vacancies.from_salary min_salary_in_RUB, vacancies.to_salary max_salary_in_RUB, vacancies.url
                            FROM employers 
                            JOIN vacancies ON vacancies.employer_id=employers.id''')
                results = cur.fetchall()
                return '\n'.join(str(result) for result in results)

    def get_avg_salary(self):
        '''получить среднюю зарплату по вакансиям'''
        with psycopg2.connect(**self.credentials) as conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT ROUND((AVG(from_salary) + AVG(to_salary)) / 2, 2)
                            FROM vacancies''')
                result = cur.fetchone()
                return str(result)[10:-4]


    def get_vacancies_with_higher_salary(self):
        '''получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям'''
        with psycopg2.connect(**self.credentials) as conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT * FROM vacancies
                            WHERE from_salary > (SELECT AVG(from_salary) FROM vacancies)
                            OR to_salary > (SELECT AVG(to_salary) FROM vacancies)''')
                results = cur.fetchall()
                return '\n'.join(str(result) for result in results)


    def get_vacancies_with_keyword(self, keyword:str):
        '''получение список всех вакансий, в названии которых содержатся переданные в метод слова, например python'''
        cap_key = keyword.lower()
        key = keyword.capitalize()
        with psycopg2.connect(**self.credentials) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""SELECT * FROM vacancies
                            WHERE vacancy_name LIKE '%{cap_key}%' OR vacancy_name LIKE '%{key}%' OR 
                            requirement LIKE '%{cap_key}%' OR requirement LIKE '%{key}%'""")
                results = cur.fetchall()
                return '\n'.join(str(result) for result in results)
