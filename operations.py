from sql_connector import execute_query
from decouple import config


def initial_site_registration(site_data, url, tags):
    site_data = str(site_data).replace("'", '"')
    site_check_query = f"select * from {config('LOG_TABLE')} where site='{url}'"
    check_site = execute_query(site_check_query)

    if len(check_site) > 0:
        return check_site[0]['id'], False
    else:
        register_site_query = f"INSERT INTO {config('LOG_TABLE')} (site,last_fetched_id, site_data, registration_date) VALUES('{url}',-1,'{site_data}',now());"
        execute_query(register_site_query)
        check_created_site = execute_query(site_check_query)

        return check_created_site[0]['id'], True