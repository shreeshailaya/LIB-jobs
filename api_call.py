from decouple import config
from utility import send_email_notification, publish_post, tag_generator
from sql_connector import execute_query
import constants
from transformation.transform import transformer, message_creator
from datetime import datetime, timedelta
import requests 
from social.notifications import telegram_bot


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
        self.tags = tags
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
                send_email_notification(subject="Error while creating DB connection", msg = f"""Unable to access url---Status code {response.status_code} --->{url}""")
                return None
        except requests.exceptions.RequestException as e:
            # If there's an error during the request, print the error
            print("Error:", e)
            send_email_notification(subject= f"Error accessing API for {self.url}", msg=f"Error while accessing API -->{e}")
            return None
        
    def dataFinishing(self, json_data):
        try:
            current_time = datetime.now()
            offset_time = current_time - timedelta(days=15)
            post_ids_list = []
            last_fetched_query = f"select last_fetched_id from {config('LOG_TABLE')} where site = '{constants.URL}'"
            last_fetched_id = execute_query(last_fetched_query)
            last_fetched_id = last_fetched_id[0]["last_fetched_id"]
            post_title_list = {}
            
            for post in json_data:
                try:
                    # Safely get post data with defaults
                    post_id = post.get("id")
                    post_date = post.get("date")
                    title_data = post.get("title", {})
                    content_data = post.get("content", {})
                    
                    title = title_data.get("rendered", "")
                    content = content_data.get("rendered", "")
                    
                    if not all([title, content]):
                        print(f"Skipping post {post_id}: Missing title or content")
                        continue
                        
                    if self.otl:
                        if datetime.fromisoformat(post_date) < offset_time:
                            content = transformer(content)
                            post_ids_list.append(post_id)
                            self.tags = tag_generator(title=title, tags=self.tags)
                            slug, link, r_content, agani_url = publish_post(post_content=content, title=title, tags=self.tags)
                            
                            if all([slug, link, r_content, agani_url]):
                                post_title_list[slug] = link
                            else:
                                print(f"Failed to publish post {post_id}: Missing required data")
                        else:
                            print(f"Post {post_id} is too recent, skipping")
                    else:
                        if int(post_id) > last_fetched_id:
                            content = transformer(content)
                            post_ids_list.append(post_id)
                            self.tags = tag_generator(title=title, tags=self.tags)
                            slug, link, r_content, agani_url = publish_post(tags=self.tags, post_content=content, title=title)
                            
                            if all([slug, link, r_content, agani_url]):
                                try:
                                    # Create message using message_creator
                                    telegram_message = message_creator(title=title, url=link, content={"raw": r_content})
                                    telegram_bot(title=telegram_message, url=link, content=agani_url)
                                    post_title_list[slug] = link
                                except Exception as telegram_error:
                                    print(f"Error sending Telegram message for post {post_id}: {str(telegram_error)}")
                            else:
                                print(f"Failed to publish post {post_id}: Missing required data")
                        else:
                            print(f"Post {post_id} already processed, skipping")
                            
                except Exception as e:
                    print(f"Error processing post {post_id}: {str(e)}")
                    print(f"Post data: {post}")
                    continue
                    
            if post_ids_list:
                max_of_ids = max(post_ids_list)
                number_of_posts = len(post_ids_list)
                update_log_table_query = f"UPDATE {config('LOG_TABLE')} SET last_fetched_id = {max_of_ids}, total_no_of_posts_fetched = total_no_of_posts_fetched+{number_of_posts} WHERE site = '{constants.URL}';"
                execute_query(update_log_table_query)
                
            if post_title_list:
                if self.otl:
                    send_email_notification(subject=f"OTL DATA FETCHED FOR {constants.URL}", msg=post_title_list)
                else:
                    send_email_notification(subject=f"Todays Jobs from {constants.URL}", msg=post_title_list)
                    
        except Exception as e:
            print(f"Error in dataFinishing: {str(e)}")
            send_email_notification(subject="Error in dataFinishing", msg=str(e))

                
