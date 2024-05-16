from decouple import config
from utility import send_email_notification
import requests 

class ApiCall():

    def convertURL(self, url):
        self.get_post_api_url = url+"wp-json/wp/v2/posts"
        return self.get_post_api_url
    
    def makeApiRequest(self, url, tags):
        url = self.convertURL(url)
        try:
            response = requests.get(url)
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
        for key in json_data:
            with open('abcd.json', "a", encoding='UTF-8') as file:
                # Append data to the file
                file.write("\n")  # Add a newline before appending if needed
                file.write(str(key['slug']))
                break
                