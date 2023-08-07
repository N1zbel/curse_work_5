import requests


def get_vacancies(keyword, per_page=10):
    url = 'https://api.hh.ru/vacancies'

    params = {
        'text': keyword,
        'per_page': per_page,
        'only_with_salary': True
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data["items"]
    else:
        print(f"Ошибка при запросе к API hh.ru: {response.status_code}")
        return []
