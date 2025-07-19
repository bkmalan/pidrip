import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import json
load_dotenv()  # Load .env file
# pip install python-telegram-bot --upgrade

BOT_TOKEN = os.getenv("BOT_TOKEN")


def update_state(value: str):
    with open("state.json", "w+") as f:
        json.dump({"state": value}, f)
    return value


def update_rain_state(value: str):
    with open("rain.json", "w+") as f:
        json.dump({"state": value}, f)
    return value


def get_state():
    try:
        with open("state.json") as f:
            return json.load(f).get("state")
    except FileNotFoundError:
        return None


def get_rain_state():
    try:
        with open("rain.json") as f:
            return json.load(f).get("state")
    except FileNotFoundError:
        return None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    words = update.message.text.split(' ')
    if words[0].lower() not in ['get', 'set', 'rain']:
        await update.message.reply_text("❌ Stop wasting my time!")
        return
    if words[0].lower() == 'get':
        await update.message.reply_text(f"Current state: {get_state()}\nRain state: {get_rain_state()}")
        return
    if words[0].lower() == 'set' and words[1].lower() in ['on', 'off']:
        await update.message.reply_text(f"Current state: {update_state(words[1].lower())}")
        return
    if words[0].lower() == 'rain' and words[1].lower() in ['on', 'off']:
        await update.message.reply_text(f"Current rain state: {update_rain_state(words[1].lower())}")
        return

    print(
        f"Message from {update.effective_user.first_name}: {update.message.text}")
    await update.message.reply_text("Invalid input! Please use 'get' or 'set <on/off>'.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running...")
    app.run_polling()
