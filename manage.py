import json
from decouple import config
from api_call import ApiCall
from operations import initial_site_registration
api_call = ApiCall()
if __name__ == '__main__':
    env_variables = config("SITES_DATA")
    env_variables = json.loads(env_variables)
    for key in env_variables:
        url = env_variables[key]["url"]
        tags = env_variables[key]["tags"]
        site_id, otl = initial_site_registration(site_data=env_variables, url=url, tags=tags)
        api_call.makeApiRequest(url=url, tags=tags, site_id=site_id, otl = otl)
