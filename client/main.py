
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackQueryHandler
from dotenv import load_dotenv
import os
from api.user import UserApiService
from bot.commands import start

load_dotenv()

SERVER_URL = os.getenv('SERVER_URL')
TOKEN = os.getenv('BOT_TOKEN')

# ADDING_EVENT, EDITING_DATE, CHOOSING_EVENT = range(3)

# events = []

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text("Hello! Use /add to add an event or /edit to edit an event.")

# async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     await update.message.reply_text("Please reply with the event name.")
#     return ADDING_EVENT

# async def receive_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     event_name = update.message.text
#     events.append(event_name)
#     await update.message.reply_text(f"Event '{event_name}' added!")
#     return ConversationHandler.END

# async def edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     await update.message.reply_text("Please reply with the date of the event you want to edit.")
#     return EDITING_DATE

# async def receive_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     date = update.message.text
#     context.user_data['edit_date'] = date
    
#     if not events:
#         await update.message.reply_text("No events to edit.")
#         return ConversationHandler.END

#     keyboard = [[InlineKeyboardButton(event, callback_data=event)] for event in events]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     await update.message.reply_text("Select an event to edit:", reply_markup=reply_markup)
#     return CHOOSING_EVENT

# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     query = update.callback_query
#     await query.answer()
#     selected_event = query.data
#     await query.edit_message_text(text=f"Selected event: {selected_event}")
#     # You can now proceed to edit the event details as needed

# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     await update.message.reply_text("Operation cancelled.")
#     return ConversationHandler.END

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    user_api_service = UserApiService(SERVER_URL + "user/")
    application.bot_data['user_api_service'] =  user_api_service

    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler('add', add), CommandHandler('edit', edit)],
    #     states={
    #         ADDING_EVENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_event)],
    #         EDITING_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_date)],
    #         CHOOSING_EVENT: [CallbackQueryHandler(button)],
    #     },
    #     fallbacks=[CommandHandler('cancel', cancel)],
    # )

    application.add_handler(CommandHandler('start', start))
    # application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()