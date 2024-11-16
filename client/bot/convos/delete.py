from typing import Any, List, Optional
from datetime import datetime
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
import requests


STATE_0 = 10


def check_day(date_str):

    # check if date_str is in yyyy-mm-dd format. If it is not, ValueError will be raised
    datetime.strptime(date_str, "%Y-%m-%d")
    return date_str


def parse_callback(callback_data):
    event_id, event_name = callback_data.split(":", 1)
    return event_id, event_name


def prepare_keyboard(
    entries: List[Optional[Any]], field: str = "event_name", id_field: str = "event_id"
) -> InlineKeyboardMarkup:
    keyboard = []
    print(entries)
    for entry in entries:
        print(entry)
        callback_data = f"{entry[id_field]}:{entry[field]}"
        button = InlineKeyboardButton(entry[field], callback_data=callback_data)
        keyboard.append([button])
    return InlineKeyboardMarkup(keyboard)


async def send_choose_event_message(
    update: Update, entries: List[Optional[Any]]
) -> None:
    keyboard = prepare_keyboard(entries)
    await update.message.reply_text(
        "Please choose the event to delete", reply_markup=keyboard
    )


async def select_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    date_str = update.message.text
    try:
        date_str = check_day(date_str)
        event_api_service = context.bot_data.get("event_api_service")
        res = event_api_service.get_user_events_day(
            update.message.from_user.id, date_str
        )
        if res["status_code"] == 200:
            await send_choose_event_message(update, res["data"])
        elif res["status_code"] == 404:
            if res["data"]["message"] == "User not found":
                await update.message.reply_text("Please press /start first.")

            else:
                await update.message.reply_text(
                    "There are no events in this day! Please enter another command."
                )
        else:
            await update.message.reply_text(
                "An error occured! Please try /delete again."
            )
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text(
            "Please enter date as yyyy-mm-dd! Please re-type the date."
        )
        return STATE_0
    except requests.exceptions.RequestException:
        await update.message.reply_text("An error occured! Please try /delete again.")
        return ConversationHandler.END


async def delete_event_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    callback_data = update.callback_query.data
    event_id, event_name = parse_callback(callback_data)
    event_api_service = context.bot_data.get("event_api_service")
    try:
        res = event_api_service.delete_event(event_id)
        if res["status_code"] == 200:
            await update.callback_query.message.reply_text(
                f"Event: {event_name} has been deleted."
            )
        elif res["status_code"] == 400:
            await update.message.reply_text(
                "Event not found! Please try /delete again."
            )
        else:
            await update.message.reply_text(
                "An error occured! Please try /delete again."
            )
        # Issue: ConversationHandler.END here not working, thus the delete conversation is ended in the select_event func above
        return ConversationHandler.END
    except requests.exceptions.RequestException:
        await update.message.reply_text("An error occured! Please try /delete again.")
        return ConversationHandler.END
