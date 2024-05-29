import smtplib
import ast
import json
import requests
import constants
from decouple import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_notification(msg):
    # Email configuration
    sender_email = config('ALERT_EMAIL')
    receiver_email = config('ADMIN_EMAIL')
    password = config('EMAIL_PASSWORD')

    # Create message container
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "ALERT FROM LIB-jobs"

    # Email content
    body = msg
    message.attach(MIMEText(body, "plain"))

    # Connect to SMTP server (Gmail)
    '''
    with smtplib.SMTP_SSL(config('EMAIL_SERVER'), config('EMAIL_PORT')) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    '''
    print(f"Email sent successfully! {msg}")

def publish_post(title,post_content, tags):        
    # Create a new post data
    new_post_data = {
        'title': title,
        'content': post_content,
        'status': 'publish',
        "categories": json.loads(tags),
        # 'meta':{
        # 'company_name':'abc',
        # 'job___':"zxc"
        # }
    }

    # Make a POST request to create a new post
    post_url = f'https://{config("HOST_NAME")}/jobs/wp-json/wp/v2/posts'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {config('WP_TOKEN')}"
    }

    response = requests.post(post_url, headers=headers, json=new_post_data)

    if response.status_code == 201:
        print('Post created successfully.')
        print('New post ID:', response.json()['id'])
    else:
        print('Error creating the post:', response.status_code, response.text)

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
    return tags
