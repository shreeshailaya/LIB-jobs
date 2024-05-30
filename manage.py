import json
import constants
from decouple import config
from api_call import ApiCall
from operations import initial_site_registration
from utility import send_email_notification
api_call = ApiCall()
if __name__ == '__main__':
    env_variables = config("SITES_DATA")
    env_variables = json.loads(env_variables)
    try:
        for key in env_variables:
            url = env_variables[key]["url"]
            constants.URL = url
            tags = env_variables[key]["tags"]
            site_id, otl = initial_site_registration(site_data=env_variables, url=url, tags=tags)
            api_call.makeApiRequest(url=url, tags=tags, site_id=site_id, otl = otl)
    except Exception as e:
        print(e)
        send_email_notification(subject="Script Failed Error ", msg=e)