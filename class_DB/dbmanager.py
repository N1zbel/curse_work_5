import psycopg2


class DBManager:
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        self.cur = self.conn.cursor()



    # Запись данных в таблицу с инфой о работодателе
    def insert_employer(self, name, url):
        self.cur.execute("INSERT INTO employers (company_name, url) VALUES (%s, %s) RETURNING id", (name, url))
        self.conn.commit()
        return self.cur.fetchone()[0]

    # Запись данных в таблицу вакансий
    def insert_vacancy(self, employer_id, title, salary, description, url):
        self.cur.execute(
            "INSERT INTO vacancies (employer_id, title, salary, description, url) VALUES (%s, %s, %s, %s, %s)",
            (employer_id, title, salary, description, url))
        self.conn.commit()

    # Получает список всех компаний и количество вакансий у каждой компании.
    def get_companies_and_vacancies_count(self):
        self.cur.execute("""
            SELECT employers.company_name, COUNT(vacancies.id) as vacancy_count
            FROM employers
            LEFT JOIN vacancies ON employers.id = vacancies.employer_id
            GROUP BY employers.company_name
        """)
        return self.cur.fetchall()

    # Получает список всех вакансий из таблицы.
    def get_all_vacancies(self):
        self.cur.execute("""
            SELECT employers.company_name, vacancies.title, vacancies.salary, vacancies.url
            FROM employers
            JOIN vacancies ON employers.id = vacancies.employer_id
        """)
        return self.cur.fetchall()

    # Получает среднюю зарплату по вакансиям из таблицы.
    def get_avg_salary(self):
        self.cur.execute("""
            SELECT AVG(CAST(REPLACE(vacancies.salary, ' ', '') AS INTEGER)) as avg_salary
            FROM vacancies
            WHERE vacancies.salary IS NOT NULL
        """)
        return self.cur.fetchone()[0]

    # Получает вакансии с зарплатой выше средней из таблицы.

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cur.execute("""
            SELECT employers.company_name, vacancies.title, vacancies.salary, vacancies.url
            FROM employers
            JOIN vacancies ON employers.id = vacancies.employer_id
            WHERE CAST(REPLACE(vacancies.salary, ' ', '') AS INTEGER) > %s
        """, (avg_salary,))
        return self.cur.fetchall()

    # Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”
    def get_vacancies_with_keyword(self, keyword):
        self.cur.execute("""
            SELECT employers.company_name, vacancies.title, vacancies.salary,vacancies.description, vacancies.url
            FROM employers
            JOIN vacancies ON employers.id = vacancies.employer_id
            WHERE vacancies.description ILIKE %s
        """, ('%' + keyword + '%',))
        return self.cur.fetchall()

    def close(self):
        self.conn.close()
