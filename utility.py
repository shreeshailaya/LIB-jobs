import smtplib
import time
import datetime
import ast
import json
import requests
import constants
from decouple import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


current_timestamp = time.time()
current_timestamp = datetime.datetime.fromtimestamp(current_timestamp)

def send_email_notification(subject, msg):
    # Email configuration
    sender_email = config('ALERT_EMAIL')
    receiver_email = config('ADMIN_EMAIL')
    password = config('EMAIL_PASSWORD')

    # Create message container
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = str(subject)

    # Email content
    body = str(msg)
    message.attach(MIMEText(body, "plain"))

    # Connect to SMTP server (Gmail)
    
    with smtplib.SMTP_SSL(config('EMAIL_SERVER'), config('EMAIL_PORT')) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    
    print(f"Email sent successfully! {msg}")

def publish_post(title, post_content, tags):        
    try:
        # Create a new post data
        new_post_data = {
            'title': title,
            'content': post_content,
            'status': 'publish',
            "type": "post",
            "categories": json.loads(tags),
            "comment_status": "closed"
        }

        # Make a POST request to create a new post
        post_url = f'https://{config("HOST_NAME")}/jobs/wp-json/wp/v2/posts'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {config('WP_TOKEN')}"
        }

        response = requests.post(post_url, headers=headers, json=new_post_data)
        
        if response.status_code == 201:
            data = response.json()
            print('Post created successfully.')
            print(f'{str(current_timestamp)} New post ID:', data.get('id'))
            
            # Create Agani URL with post ID
            agani_url = f"https://aganiai.com/job/{data.get('id')}"
            
            # Add AI preparation button to the post content
            ai_button = f'''
            <div style="text-align: center; margin: 20px 0;">
                <a href="{agani_url}" style="display: inline-block; padding: 12px 25px; background: linear-gradient(45deg, #FF6B6B, #FF8E8E); color: white; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: all 0.3s ease; border: none; cursor: pointer;">
                    🔥 Mock Interview with Aganiai.com
                </a>
            </div>
            '''
            
            # Update the post with the AI button
            updated_content = post_content + ai_button
            update_data = {
                'content': updated_content
            }
            
            # Make a PUT request to update the post
            update_url = f'{post_url}/{data.get("id")}'
            update_response = requests.post(update_url, headers=headers, json=update_data)
            
            if update_response.status_code == 200:
                print('Post updated with AI button successfully.')
                return (
                    data.get("title", {}).get("rendered", ""),
                    data.get("link", ""),
                    updated_content,
                    agani_url
                )
            else:
                print('Error updating post with AI button:', update_response.status_code)
                return None, None, None, None
        else:
            print(f'{str(current_timestamp)} Error creating the post:', response.status_code, response.text)
            return None, None, None, None
            
    except Exception as e:
        print(f'Error in publish_post: {str(e)}')
        return None, None, None, None

def tag_generator(title, tags):
    title = title.lower()
    tags = str(tags)
    tags = ast.literal_eval(tags.replace('"',"'"))
    tags_config = config("TAGS")
    tags_config = json.loads(tags_config)
    for key in tags_config:
        list_keywords = tags_config[key]
        list_keywords=ast.literal_eval(list_keywords)
        contains_keywords = any(keyword.lower() in title for keyword in list_keywords)
        if contains_keywords:
            tags.append(key)
    tags = tuple(tags)
    tags = str(list(tags))
    return tags.replace("'",'')
