from datetime import datetime
from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
import requests

STATE_0 = 00


def parse_event(event_str):
    date_str, event_name = event_str.split(" ", 1)
    # check if date_str is in yyyy-mm-dd format. If it is not, ValueError will be raised
    datetime.strptime(date_str, "%Y-%m-%d")
    return date_str, event_name


async def receive_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    event = update.message.text
    try:
        event_date, event_name = parse_event(event)
        event_api_service = context.bot_data.get("event_api_service")
        res = event_api_service.add_event(
            update.message.from_user.id, event_name, event_date
        )
        if res["status_code"] == 200:
            await update.message.reply_text(
                f"Event '{event_name}' on '{event_date}' added!"
            )
        elif res["status_code"] == 404:
            await update.message.reply_text("Please press /start first.")
        else:
            await update.message.reply_text("An error occured! Please try /add again.")
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text(
            "The format is <yyyy-mm-dd> <event name>. Eg. 2000-01-01 Lunch with family. Please re-type."
        )
        return STATE_0
    except requests.exceptions.RequestException:
        await update.message.reply_text("An error occured! Please try /add again.")
        return ConversationHandler.END
