from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import TelegramError
from decouple import config
from utility import send_email_notification
import requests

def telegram_bot(title, url, content):
    try:
        BOT_TOKEN = config('telegram_bot_token')
        CHANNEL_ID = config('telegram_channel')
        
        # Create keyboard markup with styled buttons
        keyboard = [
            [InlineKeyboardButton("📝 Apply for Job", url=url)],
            [InlineKeyboardButton(f"🤖 Mock Interview with {config('agani_ai_url')}", url=content)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Prepare the message data
        message_data = {
            'chat_id': CHANNEL_ID,
            'text': title,
            'reply_markup': reply_markup.to_dict(),
            'disable_web_page_preview': True
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