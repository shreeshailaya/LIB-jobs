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
    youtube_link = config("youtube_link")
    

    # Replace WhatsApp links
    if whatsapp_link:
        for a in soup.find_all('a', href=True):
            url = a['href']
            if url.lower().startswith('https://whatsapp.com'):
                a['href'] = whatsapp_link
    
    if youtube_link:
        for a in soup.find_all('a', href=True):
            url = a['href']
            if url.lower().startswith('https://www.youtube.com'):
                a['href'] = youtube_link

    # Replace Instagram links
    if instagram_link:
        for a in soup.find_all('a', href=True):
            url = a['href']
            if url.lower().startswith('https://instagram.com'):
                a['href'] = instagram_link
    
    if telegram_link:
        for a in soup.find_all('a', href=True):
            url = a['href']
            if url.lower().startswith('https://telegram.dog') or url.lower().startswith('https://telegram.me/'):
                a['href'] = telegram_link

    # Replace website links
    if website_link:
        for a in soup.find_all('a', href=True):
            url = a['href']
            if url.startswith(constants.URL) or url.lower().startswith('https://www.facebook.com'):
                a['href'] = website_link
    return soup

def remove_html_tags(html):
    # Parse the HTML content
    html = html['raw']
    soup = BeautifulSoup(html, "lxml")
    # Remove any script and style tags
    for script in soup(["script", "style"]):
        script.extract()
    # Get the plain text
    text = soup.get_text()
    return text

def message_creator(title, url, content):
    content =  remove_html_tags(content)
    words = content.split()
    selected_words = words[:55]
    content = ' '.join(selected_words)
    message = f"{title} \n \n{content} \n \n{url}"
    return message