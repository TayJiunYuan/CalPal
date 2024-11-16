from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes


def events_to_md(data, month_str):
    year = int(month_str[0:4])
    month = int(month_str[5:7])
    reply = ""
    for day_str in data:
        day = int(day_str)
        date = datetime(year, month, day)
        date_str = date.strftime("%Y-%m-%d").replace("-", "\-")  # escape hyphen
        day_of_week = date.strftime("%a")
        reply += f"*{date_str} \({day_of_week}\)* \n"
        for event in data[day_str]:
            reply += f"{event["event_name"]} \n"
        reply += "\n"
        print(reply)
    return reply


def events_to_md_day(data, date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    date_str = date.strftime("%Y-%m-%d").replace("-", "\-")  # escape hyphen
    day_of_week = date.strftime("%a")
    reply = f"*{date_str} \({day_of_week}\)* \n"
    for event in data:
        reply += f"{event["event_name"]} \n"
    return reply


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    open_ai_service = context.bot_data.get("open_api_service")
    event_api_service = context.bot_data.get("event_api_service")
    obj = open_ai_service.get_response(message)
    print(obj)
    if obj["action"] == "help":
        await update.message.reply_text(
            "Welcome to CalPal 1.0 :) \n\n"
            "/add - Add an event\n"
            "/view_month - View events in the month\n"
            "/delete - Delete an event\n\n"
            "Or, just type any message to call our AI chatbot! \n"
            'For example, ask: "What events do I have today?"'
        )
    if obj["action"] == "add":
        res = event_api_service.add_event(
            update.message.from_user.id, obj["event_name"], obj["event_date"]
        )
        if res["status_code"] == 200:
            await update.message.reply_text(
                f"Event '{obj["event_name"]}' on '{obj["event_date"]}' added!"
            )
        elif res["status_code"] == 404:
            await update.message.reply_text("Please press /start first.")
        else:
            await update.message.reply_text("An error occured! Please try again.")
    if obj["action"] == "view_month":
        res = event_api_service.get_user_events_month(
            update.message.from_user.id, obj["event_month"]
        )
        if res["status_code"] == 200:
            await update.message.reply_text(
                events_to_md(res["data"], obj["event_month"]), parse_mode="Markdownv2"
            )
        elif res["status_code"] == 404:
            if res["data"]["message"] == "User not found":
                await update.message.reply_text("Please press /start first.")
            else:
                await update.message.reply_text("There are no events!")
    if obj["action"] == "view_day":
        res = event_api_service.get_user_events_day(
            update.message.from_user.id, obj["event_date"]
        )
        if res["status_code"] == 200:
            await update.message.reply_text(
                events_to_md_day(res["data"], obj["event_date"]),
                parse_mode="Markdownv2",
            )
        elif res["status_code"] == 404:
            if res["data"]["message"] == "User not found":
                await update.message.reply_text("Please press /start first.")
            else:
                await update.message.reply_text("There are no events!")
    if obj["action"] == "prompt":
        await update.message.reply_text(obj["message"])
