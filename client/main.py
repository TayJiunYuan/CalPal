from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
)
from dotenv import load_dotenv
import os
from api.user import UserApiService
from api.event import EventApiService
from api.openai import OpenAIService
from bot import commands
from bot import message

from bot.convos import add, view_month, delete

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")
TOKEN = os.getenv("BOT_TOKEN")
OPEN_API_KEY = os.getenv("OPEN_API_KEY")


def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    user_api_service = UserApiService(SERVER_URL + "user")
    application.bot_data["user_api_service"] = user_api_service

    event_api_service = EventApiService(SERVER_URL + "event")
    application.bot_data["event_api_service"] = event_api_service

    open_api_service = OpenAIService(OPEN_API_KEY=OPEN_API_KEY)
    application.bot_data["open_api_service"] = open_api_service

    add_handler = CommandHandler("add", commands.add_command)
    month_handler = CommandHandler("view_month", commands.view_month_command)
    delete_handler = CommandHandler("delete", commands.delete_command)

    conv_handler = ConversationHandler(
        entry_points=[add_handler, month_handler, delete_handler],
        states={
            add.STATE_0: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, add.receive_event)
            ],
            view_month.STATE_0: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, view_month.view_month)
            ],
            delete.STATE_0: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, delete.select_event)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", commands.cancel_command),
        ],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", commands.start_command))
    application.add_handler(CommandHandler("help", commands.help_command))
    application.add_handler(CallbackQueryHandler(delete.delete_event_callback))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message.handle_message)
    )

    print("CalPal Started")
    application.run_polling()


if __name__ == "__main__":
    main()
