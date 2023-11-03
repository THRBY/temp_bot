from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineQueryResultArticle, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    CommandHandler, 
    Application, 
    ContextTypes, 
    MessageHandler, 
    ConversationHandler,
    CallbackQueryHandler,
    filters)
import requests
from keys import TOKEN, API_KEY_WEATHER

# API-ключ от OpenWeatherMap
API_KEY = API_KEY_WEATHER

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    city_name = update.message.text

    # Формирование запроса к OpenWeatherMap API
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=ru&units=metric&appid={API_KEY}"
    response = requests.get(url)
    weather_data = response.json()

    if weather_data.get('cod') == 200:
        # Получение данных о погоде
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']

        # Отправка сообщения пользователю
        await update.message.reply_text(f'Сейчас в {city_name} {description}.\n Температура {temperature} °C.\n Влажность {humidity}%.')
    else:
        await update.message.reply_text("Город не найден. Попробуйте другой город.")