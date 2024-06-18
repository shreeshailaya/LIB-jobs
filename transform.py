import re
from bs4 import BeautifulSoup
import constants
from decouple import config
from utility import send_email_notification


def transformer(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        soup = link_transformer(soup)
        soup = remove_square_bracket_text(soup)
    except Exception as e:
        print(e)
        send_email_notification(subject="Error in Transformation", msg=e)

    return str(soup)


def remove_square_bracket_text(soup):
    for text in soup.find_all(string=True):
        # Replace text inside square brackets with an empty string
        new_text = re.sub(r'\[.*?\]', '', text)
        if new_text != text:
            text.replace_with(new_text)
    return soup

def link_transformer(soup):
    website_link = config("HOST_NAME")
    whatsapp_link= config("whatsapp_link")
    instagram_link = config("instagram_link")
    telegram_link = config("telegram_link")
    

    # Replace WhatsApp links
    if whatsapp_link:
        for a in soup.find_all('a', href=True):
            url = a['href']
            if url.lower().startswith('https://whatsapp.com'):
                a['href'] = whatsapp_link

    # Replace Instagram links
    if instagram_link:
        for a in soup.find_all('a', href=True):
            url = a['href']
            if url.lower().startswith('https://instagram.com'):
                a['href'] = instagram_link
    
    if telegram_link:
        for a in soup.find_all('a', href=True):
            url = a['href']
            if url.lower().startswith('https://telegram.dog'):
                a['href'] = telegram_link

    # Replace website links
    if website_link:
        for a in soup.find_all('a', href=True):
            url = a['href']
            if url.startswith(constants.URL):
                a['href'] = website_link
    return soup
