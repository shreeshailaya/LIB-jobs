from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from telegram.error import TelegramError
from transformation.transform import message_creator  
from decouple import config
from utility import send_email_notification

def telegram_bot(title, content, url):
    BOT_TOKEN = config('telegram_bot_token')
    CHANNEL_ID = config('telegram_channel')
    message = message_creator(title=title, content=content, url=url)
    bot = Bot(token=BOT_TOKEN)

    async def send_message(text):
        try:
            # Create an inline keyboard with a button
            keyboard = [[InlineKeyboardButton("Follow on Instagram", url=config("instagram_link"))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.send_message(chat_id=CHANNEL_ID, text=text, reply_markup=reply_markup)
            print(f"Message sent to channel {CHANNEL_ID}")
        except TelegramError as e:
            send_email_notification(subject="Telegram Message Fails", msg=e)
            print(f"Failed to send message telegram: {e}")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(send_message(text=message))
    except KeyboardInterrupt:
        pass