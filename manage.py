import json
from decouple import config
from api_call import ApiCall
api_call = ApiCall()
if __name__ == '__main__':
    env_variables = config("SITES_DATA")
    env_variables = json.loads(env_variables)
    for key in env_variables:
        url = env_variables[key]["url"]
        tags = env_variables[key]["tags"]
        api_call.makeApiRequest(url=url, tags=tags)
