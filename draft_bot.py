import logging
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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# TOKEN-клют от телеграм бота
TOKEN = TOKEN

# API-ключ от OpenWeatherMap
OWN_TOKEN = OWN_TOKEN

MENU, ITEM_SELECTED, SCHEDULER = range(3)

#water
WEATHER = range(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот ... . Могу подказать погоду')
    
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
            description = weather_data['weather'][0]['description']
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            await update.message.reply_text(f'Текущая погода в {location}:\n Температура: {temperature}°C\n Статус: {description}\n Влажность {humidity}%.')
            
        except Exception as e:
            await update.message.reply_text(f"Произошла ошибка при получении погоды: {e}")  
        
    else:
        await update.message.reply_text("Город не найден. Попробуйте другой город.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    """Cancels and ends the conversation."""

    user = update.message.from_user

    logger.info("User %s canceled the conversation.", user.first_name)

    await update.message.reply_text("Пока!", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def main() -> None:    
    application = Application.builder().token(TOKEN).build()
       
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, weather))
    application.run_polling()

if __name__ == "__main__":
    main()