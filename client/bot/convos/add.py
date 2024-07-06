from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
)
import requests
from .helpers import parse_event
from bot import commands

state0 = 7


async def receive_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    event = update.message.text
    try:
        event_date, event_name = parse_event(event)
        event_api_service = context.bot_data.get("event_api_service")
        res = event_api_service.add_event(
            update.message.from_user.id, event_name, event_date
        )
        if res["status_code"] == 500:
            await update.message.reply_text("An error occured! Please try /add again.")
        elif res["status_code"] == 400:
            await update.message.reply_text("Please press /start first.")
        else:  # status_code = 200
            await update.message.reply_text(
                f"Event '{event_name}' on '{event_date}' added!"
            )
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text(
            "Please enter date as yyyy-mm-dd! Try again or /cancel to cancel."
        )
        return state0
    except requests.exceptions.Timeout:
        await update.message.reply_text("An error occured! Please try /add again.")
        return ConversationHandler.END


async def end_convo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        f"Ending current command. Please press {update.message.text} again."
    )
    return ConversationHandler.END
