from telegram import (
    Update,
    ForceReply,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton
)
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
from .helpers import parse_event, check_day
from bot import commands

from typing import Any, List, Optional, Sequence, Union

state0 = 10

def parse_callback(callback_data):
    event_id, event_name = callback_data.split(":",1)
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

async def send_choose_event_message(update: Update, entries: List[Optional[Any]]) -> None:
    keyboard = prepare_keyboard(entries)
    await update.message.reply_text("Please choose the event to delete", reply_markup=keyboard)


async def select_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    date_str = update.message.text
    print(date_str)
    try:
        date_str = check_day(date_str)
        event_api_service = context.bot_data.get("event_api_service")
        res = event_api_service.get_user_events_day(
            update.message.from_user.id, date_str
        )
        if res["status_code"] == 500:
            await update.message.reply_text(
                "An error occured! Please try /delete again."
            )
            return ConversationHandler.END
        elif res["status_code"] == 400:
            await update.message.reply_text("Please press /start first.")
            return ConversationHandler.END
        elif res["status_code"] == 404:
            await update.message.reply_text("There are no events in this day!")
            return ConversationHandler.END
        else:  # status_code = 200
            await send_choose_event_message(update, res['data'])
            return ConversationHandler.END
    except ValueError as e:
        await update.message.reply_text("Please enter date as yyyy-mm-dd! Try again")
        print(e)
        return state0
    except requests.exceptions.Timeout:
        await update.message.reply_text("An error occured! Please try /add again.")
        return ConversationHandler.END
    
async def delete_event_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Parses the CallbackQuery and updates the message text."""
    callback_data = update.callback_query.data
    event_id, event_name = parse_callback(callback_data)
    print(event_id)
    # Get the event API service from context
    event_api_service = context.bot_data.get("event_api_service")
    
    # Delete the event using the event ID
    res = event_api_service.delete_event(event_id)
    print(res)
    if res["status_code"] == 500:
        await update.message.reply_text("An error occured! Please try /delete again.")
        return ConversationHandler.END
    elif res["status_code"] == 400:
        await update.message.reply_text("Event not found! Please try /delete again.")
        return ConversationHandler.END
    else:  # status_code = 200
    
        # Respond to the user with the event deletion message
        await update.callback_query.message.reply_text(f"Event: {event_name} has been deleted.")
        
        # Acknowledge the callback to remove the "loading" state from the button
        await update.callback_query.answer()
        
        return ConversationHandler.END

    

