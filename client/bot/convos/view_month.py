from datetime import datetime
from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
import requests

STATE_0 = 20


def check_month(date_str):
    # check if date_str is in yyyy-mm format. If it is not, ValueError will be raised
    datetime.strptime(date_str, '%Y-%m')
    return date_str


def events_to_md(data, month_str):
    year = int(month_str[0:4])
    month = int(month_str[5:7])
    reply = ""
    for day_str in data:
        day = int(day_str)
        date = datetime(year, month, day)
        date_str = date.strftime("%Y-%m-%d").replace("-", "\-")  #escape hyphen
        day_of_week = date.strftime('%a')
        reply += f"*{date_str} \({day_of_week}\)* \n"
        for event in data[day_str]:
            reply += f"{event["event_name"]} \n"
        reply += "\n" 
        print(reply)
    return reply


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
        return STATE_0
    except requests.exceptions.RequestException:
        await update.message.reply_text("An error occured! Please try /view_month again.")
        return ConversationHandler.END
