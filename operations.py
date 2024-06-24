import asyncio
from sql_connector import execute_query
from decouple import config
from telegram import Bot
from telegram.error import TelegramError
from transform import message_creator
from utility import send_email_notification
import constants


def initial_site_registration(site_data, url, tags):
    site_data = str(site_data).replace("'", '"')
    site_check_query = f"select * from {config('LOG_TABLE')} where site='{url}'"
    check_site = execute_query(site_check_query)

    if len(check_site) > 0:
        return check_site[0]['id'], False
    else:
        register_site_query = f"INSERT INTO {config('LOG_TABLE')} (site,last_fetched_id, site_data, registration_date,total_no_of_posts_fetched) VALUES('{url}',-1,'{site_data}',now(), 0);"
        execute_query(register_site_query)
        check_created_site = execute_query(site_check_query)

        return check_created_site[0]['id'], True
    
def telegram_bot(title, content, url):
    BOT_TOKEN = config('telegram_bot_token')
    CHANNEL_ID = config('telegram_channel')
    message = message_creator(title=title, content=content, url=url)
    bot = Bot(token=BOT_TOKEN)
    async def send_message(text):
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=text)
            print(f"Message sent to channel {CHANNEL_ID}")
        except TelegramError as e:
            send_email_notification(subject=f"Failed telegram message on {constants.URL}", msg=e)
            print(f"Failed to send message telegram: {e}")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(send_message(message))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()