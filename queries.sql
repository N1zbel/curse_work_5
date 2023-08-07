-- Создание базы данных
CREATE DATABASE vacancies_db;

-- Подключение к базе данных
\c vacancies_db

-- Создание таблицы работодателей
CREATE TABLE IF NOT EXISTS employers
(
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        url TEXT
);

-- Создание таблицы вакансий
CREATE TABLE IF NOT EXISTS vacancies
(
        id SERIAL PRIMARY KEY,
        employer_id INT REFERENCES employers(id),
        title VARCHAR(255),
        salary VARCHAR(50),
        description TEXT,
        url TEXT
)

