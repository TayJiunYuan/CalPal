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
from .helpers import check_month, events_to_md

state0 = range(1)

async def view_month(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    month_str = update.message.text
    try:
        month_str = check_month(month_str)
        event_api_service = context.bot_data.get("event_api_service")
        res = event_api_service.get_user_events_month(
            update.message.from_user.id, month_str
        )
        if res["status_code"] == 200:
            await update.message.reply_text(
                events_to_md(res["data"], month_str), parse_mode='Markdownv2'
            )
        elif res["status_code"] == 404:
            if res["data"]["message"] == 'User not found':
                await update.message.reply_text("Please press /start first.")
            else:
                await update.message.reply_text("There are no events in this month! Please enter another command.")
        else:
            await update.message.reply_text("An error occured! Please try /view_month again.")
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Please enter date as yyyy-mm! Please re-type the date.")
        return state0
    except requests.exceptions.RequestException:
        await update.message.reply_text("An error occured! Please try /view_month again.")
        return ConversationHandler.END
    



