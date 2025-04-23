# telegram_bot.py

import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv
from billing import get_payment_info

# Loading data from .env
load_dotenv()

# Getting data from .env
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

async def send_telegram_message(bot, chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)

async def main():
    # Bot initialization
    bot = Bot(token=TELEGRAM_TOKEN)
    
    # Receiving payment information
    payment_info = get_payment_info()
    
    # Sending a message in Telegram
    await send_telegram_message(bot, CHAT_ID, payment_info)

if __name__ == "__main__":
    asyncio.run(main())
