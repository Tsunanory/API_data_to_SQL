from config import config
from utils import get_employers_data, get_vacancy_data, create_database, save_employers_to_database, save_vacancies_to_database
from DBManager import DBManager


key_emp = 'https://api.hh.ru/employers'
key_vac = 'https://api.hh.ru/vacancies'

def main():
    employers_ids = [
        '154', # Diasoft
        '15478', # VK
        '78638', # Тинькофф
        '3529', # СБЕР
        '87891', # HeadHunter: Казахстан
        '26624', # Positive Technologies
        '1122462', # Skyeng
        '3496985', # Астра
        '2381', # Softline
        '9498120', # Яндекс Команда для бизнеса
    ]
    params = config()

    employers = get_employers_data(key_emp, employers_ids)
    vacancies = get_vacancy_data(key_vac, employers_ids)
    create_database('vacancies', params)
    save_employers_to_database(employers, 'vacancies', params)
    save_vacancies_to_database(vacancies, 'vacancies', params)

if __name__ == '__main__':
    main()

# mng = DBManager()
# print(mng.get_companies_and_vacancies_count())
# print(mng.get_all_vacancies())
# print(mng.get_avg_salary())
# print(mng.get_vacancies_with_higher_salary())
# print(mng.get_vacancies_with_keyword('python'))
