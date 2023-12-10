import requests

async def wikipedia_page(title: str) -> str:
    language_code = 'ru'

    # Формируем URL запроса к Wikipedia API
    wikipedia_url_api = f'https://{language_code}.wikipedia.org/api/rest_v1/page/summary/{title}'

    # Отправка GET-запроса к Wikipedia API
    response = requests.get(wikipedia_url_api)

    # Проверка успешности запроса
    if response.status_code == 200:
        # Получение данных в формате JSON
        data = response.json()

        # Вывод введения страницы
        title_page = data["title"]
        all_page = data["extract"]
        return f"{title_page}\n{all_page}"
    else:
        return f"Ошибка при запросе к Wikipedia API: {response.status_code}"