from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from bot.convos import add, view_month, delete
import requests


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_api_service = context.bot_data.get("user_api_service")
        res = user_api_service.create_user(
            update.message.from_user.id, update.message.from_user.username
        )
        if res["status_code"] == 500:
            await update.message.reply_text(
                "An error occured! Please try /start again."
            )
        else:
            if res["status_code"] == 409:
                await update.message.reply_text(
                    "Welcome Back! Use /help to see the available commands or /add to add an event."
                )
            else:  # status_code 200
                await update.message.reply_text(
                    "Hello! Welcome to CalPal! Use /help to see the available commands or /add to add an event."
                )
    except requests.exceptions.Timeout:  # probably a timeout
        await update.message.reply_text("An error occured! Please try /start again.")
    return ConversationHandler.END


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.message.reply_text(
        "Please reply with the event name and event date in this format: yyyy-mm-dd event name or /cancel to cancel"
    )
    return add.STATE_0


async def view_month_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Please reply with the month you want to view in this format: yyyy-mm or /cancel to cancel"
    )
    return view_month.STATE_0


async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Please reply with the event date in this format: yyyy-mm-dd for the event you want to delete or /cancel to cancel"
    )
    return delete.STATE_0


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Welcome to CalPal 1.0 :) \n\n"
        "/add - Add an event\n"
        "/view_month - View events in the month\n"
        "/delete - Delete an event\n\n"
        "Or, just type any message to call our AI chatbot! \n"
        'For example, ask: "What events do I have today?"'
    )
    return ConversationHandler.END
