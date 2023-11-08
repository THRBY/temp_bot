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

from keys import TOKEN, API_KEY_WEATHER
from weather import weather


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# TOKEN-клют от телеграм бота
TOKEN = TOKEN

# API-ключ от OpenWeatherMap
API_KEY = API_KEY_WEATHER

MENU, ITEM_SELECTED, SCHEDULER = range(3)

#water
WEATHER = range(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот ..., для дальнейшей работы используйте команду /menu.')
    return MENU
    
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Погода", callback_data='item1')],
        [InlineKeyboardButton("Планирование", callback_data='item2')],
        [InlineKeyboardButton("Курс валюты", callback_data='item3')],
        [InlineKeyboardButton("other", callback_data='itemN')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите пункт меню:', reply_markup=reply_markup)
    
    return ITEM_SELECTED

async def item_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    query.answer()
    item = query.data
    
    if item == 'item1':
        await query.message.reply_text('Вы выбрали: "Погода". Теперь выберите город:')
        return WEATHER
    elif item == "item2":
        return SCHEDULER
    else:
        return ConversationHandler.END  

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    """Cancels and ends the conversation."""

    user = update.message.from_user

    logger.info("User %s canceled the conversation.", user.first_name)

    await update.message.reply_text("Пока!", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def main() -> None:    
    application = Application.builder().token(TOKEN).build()
    '''
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))
    '''
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [CommandHandler("menu", menu), CommandHandler("cancel", cancel)],
            ITEM_SELECTED: [CallbackQueryHandler(item_selected, pattern='^item'), CommandHandler("cancel", cancel), CommandHandler("menu", menu),],
            WEATHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, weather), CommandHandler("cancel", cancel), CommandHandler("menu", menu),],
        },
        #fallbacks=[CommandHandler("cancel", cancel)]
        fallbacks=[CommandHandler("start", start)]
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()