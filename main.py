from class_DB.dbmanager import DBManager
from api.hh_api import get_vacancies
import os
from time import sleep
from func_for_clear import func_for_clear_text

PASS = os.getenv('pgadmin')


def main():
    # Подключение к базе данных
    db_manager = DBManager(host="localhost", database="vacancies", user='postgres', password=PASS)

    # Получение данных о вакансиях с hh.ru
    vacancy_name = (input('Введите запрос для поиска вакансий : '))
    num_vacancies = int(input('Введите количество вакансий: '))
    vacancies = get_vacancies(vacancy_name, num_vacancies)

    # Заполнение базы данных данными о работодателях и вакансиях
    for vacancy in vacancies:
        employer_name = vacancy["employer"]["name"]
        employer_info = vacancy["employer"].get("alternate_url", "")
        employer_id = db_manager.insert_employer(employer_name, employer_info)

        vacancy_title = vacancy["name"]
        vacancy_salary = vacancy.get("salary", {}).get("from", "")
        url = vacancy.get("apply_alternate_url", "")
        description = vacancy['snippet']['requirement']
        description = func_for_clear_text(str(description))

        db_manager.insert_vacancy(employer_id, vacancy_title, vacancy_salary, description, url)
    print('----------------------------')
    while True:
        user_input = input(
            'Для получения списка всех вакансий с указанием названия компании, названия вакансии ,зарплаты и ссылки на вакансию - введите "1"\n'
            'Для получения Количества компаний и ваканский в них введите "2"\n'
            'Для получения средней зарплаты по вакансиям введите "3"\n'
            'Для получения вакансий с зарплатой выше среднего введите "4"\n'
            'Для получения вакансий по ключевому слову введите "5"\n'
            'Для выхода введите "0"\n:'
        )
        if user_input == '1':
            all_vacancies = db_manager.get_all_vacancies()
            print("Все вакансии :")
            for vacancy in all_vacancies:
                print(vacancy)
            timeout = input('Нажмите "enter" чтобы продолжить')
        elif user_input == '2':
            companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
            print("Количество компаний и ваканский в них :")
            for vacancy in companies_and_vacancies:
                print(vacancy)
            timeout = input('Нажмите "enter" чтобы продолжить')
        elif user_input == '3':
            avg_salary = db_manager.get_avg_salary()
            print("Средняя зарплата по всем вакансиям :", avg_salary)
            timeout = input('Нажмите "enter" чтобы продолжить')
        elif user_input == '4':
            high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            print("Вакансии с зарплатой выше средней :")
            for vacancy in high_salary_vacancies:
                print(vacancy)
            timeout = input('Нажмите "enter" чтобы продолжить')
        elif user_input == '5':
            keyword = input('Введите ключевое слово для поиска в вакансиях: ')
            keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
            print(f"Вакансии по ключевому слову - {keyword}:")
            for vacancy in keyword_vacancies:
                print(vacancy)
            timeout = input('Нажмите "enter" чтобы продолжить')
        elif user_input == '0':
            print('Программа завершена, всю информацию о вакансиях вы сможете посмотреть в таблице')
            break
        else:
            print('Неверный ввод')
            timeout = input('Нажмите "enter" чтобы продолжить')

    # Закрытие соединения с базой данных
    db_manager.close()


if __name__ == "__main__":
    main()
