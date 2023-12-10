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
from weather import weather
from wikipedia_page import wikipedia_page

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

async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send text meassage
    message_text = update.message.text.lower()

    # Checking if the message contains the keyword 'weather'
    if 'погода' in message_text:
        # Getting the name of the city
        location = message_text.split('погода', 1)[1].strip()

        weather_info = await weather(location)

        await update.message.reply_text(weather_info)
    elif 'что такое' in message_text:
        # Getting the answer of wiki
        title = message_text.split('что такое', 1)[1].strip()

        wiki_page = await  wikipedia_page(title)

        await update.message.reply_text(wiki_page)
    else:
        await update.message.reply_text("ЯННП.")

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
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, command))
    application.run_polling()

if __name__ == "__main__":
    main()