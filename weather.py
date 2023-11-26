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
from keys import TOKEN, OWN_TOKEN

# API-ключ от OpenWeatherMap
API_KEY = OWN_TOKEN

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send text meassage
    message_text = update.message.text.lower()

    # Checking if the message contains the keyword 'weather'
    if 'погода' in message_text:
        # Getting the name of the city
        location = message_text.split('погода', 1)[1].strip()

        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&lang=ru&units=metric&appid={OWN_TOKEN}"
        response = requests.get(url)
        weather_data = response.json()

        try:
            '''
            # Get current weather for the specified city
            observation = mgr.weather_at_place(location)
            w = observation.weather

            # Send weather forecast
            await update.message.reply_text(f"Текущая погода в {observation.location.name}:\n"
                                            f"Теммература: {w.temperature('celsius')['temp']}°C\n"
                                            f"Статус: {w.detailed_status}")
            '''
            
            description = weather_data['weather'][0]['description']
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            await update.message.reply_text(f'Текущая погода в {location}:\n Температура: {temperature}°C\n Статус: {description}\n Влажность {humidity}%.')
            
        except Exception as e:
            await update.message.reply_text(f"Произошла ошибка при получении погоды: {e}")  
        
    else:
        await update.message.reply_text("Город не найден. Попробуйте другой город.")