import requests
from keys import OWN_TOKEN

# API-ключ от OpenWeatherMap
OWN_TOKEN = OWN_TOKEN

async def weather(location: str) -> str:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&lang=ru&units=metric&appid={OWN_TOKEN}"
    response = requests.get(url)
    weather_data = response.json()

    try:
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        return f'Текущая погода в {location}:\n Температура: {temperature}°C\n Статус: {description}\n Влажность {humidity}%.'
    except Exception as e:
        return "Произошла ошибка при получении погоды: {e}"