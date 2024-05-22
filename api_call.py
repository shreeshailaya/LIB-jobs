from decouple import config
from utility import send_email_notification, publish_post
from datetime import datetime, timedelta
import requests 

class ApiCall():

    def convertURL(self, url):
        if self.otl:
            url = url+"wp-json/wp/v2/posts?per_page=100"
        else:
            url = url+"wp-json/wp/v2/posts"
        return url
    
    def makeApiRequest(self, url, tags, site_id, otl):
        self.otl = otl
        self.url = self.convertURL(url)
        self.site_id = site_id
        print(self.url)
        
        try:
            response = requests.get(self.url)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # If successful, return the response JSON data
                print(url, "200")
                return self.dataFinishing(response.json())
            else:
                # If unsuccessful, print an error message
                print("Error:", response.status_code)
                send_email_notification(f"""Unable to access url---Status code {response.status_code} --->{url}""")
                return None
        except requests.exceptions.RequestException as e:
            # If there's an error during the request, print the error
            print("Error:", e)
            send_email_notification(f"Error while accessing API -->{e}")
            return None
        
    def dataFinishing(self, json_data):
        current_time = datetime.now()
        offset_time = current_time - timedelta(days=15)
        print(offset_time)
        for post in json_data:
            if self.otl:
                if datetime.fromisoformat(post["date"]) < offset_time:
                    title = post["title"]["rendered"]
                    content = post["content"]["rendered"]
                    post_id = post["id"]
                    print(title, post_id)
                    publish_post(post_content=content, title=title, post_id=post_id)
                else:
                    print("no post found ")
            else:
                title = post["title"]["rendered"]
                content = post["content"]["rendered"]
                post_id = post["id"]
                publish_post(post_content=content, title=title, post_id=post_id)

                break

                

                