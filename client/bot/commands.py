from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update)
    user_api_service = context.bot_data.get('user_api_service')
    user_api_service.create_user(update.message.from_user.id, update.message.from_user.username)
    await update.message.reply_text("Hello! Welcome to CalPal! Use /add to add an event.")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
     await update.message.reply_text("Please reply with the event name and event date in this format: yyyy-mm-dd event name.")
     return add.state0



