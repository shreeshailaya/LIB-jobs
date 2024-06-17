from bs4 import BeautifulSoup
import constants
from decouple import config

class Transform():

    def link_transformer(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
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

        # Remove square brackets from strings
        # for string in soup.stripped_strings:
        #     new_string = string.replace('[', '').replace(']', '')
        #     string.replace_with(new_string)

        return str(soup)
