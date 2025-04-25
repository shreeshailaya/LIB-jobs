from telegram.ext import Application
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import TelegramError
from decouple import config
from utility import send_email_notification
import asyncio
import requests

async def send_telegram_message(bot, title, url, content, channel_id):
    try:
        # Create keyboard markup
        keyboard = [
            [InlineKeyboardButton("Apply for Job", url=url)],
            [InlineKeyboardButton("Prepare with AI", url=content)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send message using the bot
        await bot.send_message(
            chat_id=channel_id,
            text=title,
            reply_markup=reply_markup,
            parse_mode=None,
            disable_web_page_preview=True
        )
        print(f"Message sent to channel {channel_id}")
    except TelegramError as e:
        send_email_notification(subject="Telegram Message Fails", msg=str(e))
        print(f"Failed to send message to telegram: {e}")

async def run_telegram_bot(title, url, content):
    try:
        BOT_TOKEN = config('telegram_bot_token')
        CHANNEL_ID = config('telegram_channel')
        
        # Create the application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Run the message sending
        await send_telegram_message(application.bot, title, url, content, CHANNEL_ID)
        
        # Shutdown the application
        await application.shutdown()
        
    except Exception as e:
        print(f"Error in telegram_bot: {str(e)}")
        send_email_notification(subject="Telegram Bot Error", msg=str(e))

def telegram_bot(title, url, content):
    try:
        BOT_TOKEN = config('telegram_bot_token')
        CHANNEL_ID = config('telegram_channel')
        
        # Create keyboard markup with styled buttons
        keyboard = [
            [InlineKeyboardButton(" Apply for Job", url=url)],
            [InlineKeyboardButton("🔥 Mock Interview with Aganiai.com", url=content)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Prepare the message data with HTML formatting
        message_data = {
            'chat_id': CHANNEL_ID,
            'text': title,
            'reply_markup': reply_markup.to_dict(),
            'disable_web_page_preview': True,
            'parse_mode': 'HTML'  # Enable HTML formatting
        }
        
        # Send message using direct API call
        response = requests.post(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
            json=message_data
        )
        
        if response.status_code == 200:
            print(f"Message sent to channel {CHANNEL_ID}")
        else:
            error_msg = f"Failed to send message: {response.text}"
            send_email_notification(subject="Telegram Message Fails", msg=error_msg)
            print(error_msg)
            
    except Exception as e:
        print(f"Error in telegram_bot: {str(e)}")
        send_email_notification(subject="Telegram Bot Error", msg=str(e))