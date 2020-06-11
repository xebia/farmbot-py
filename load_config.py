import json
import os
from urllib.request import urlopen,Request
from urllib import parse
from shutil import copy

# Check if config exists. If not copy template to src folder
config_path = os.path.join(os.getcwd(),'config.json')
template_path = os.path.join(os.getcwd(),'farmbot/config-template.json')
if not os.path.exists(config_path):
    copy(template_path, config_path)

# Get an API token using email / password.
user_data = {'user': {'email': 'user@email.com', 'password': 'password'}}
url = 'https://my.farmbot.io/api/tokens'

# To generate the token, we POST JSON to `api/tokens`.
data = str(json.dumps(user_data)).encode('utf-8')
req = Request(url,data=data)
req.add_header('Content-Type', 'application/json')
with urlopen(req) as response:
    # It will return a JSON object...
    raw_json = response.read()
    token_data = json.loads(raw_json)

    # ... response_body.token.encoded is the important part- you will use this as
    # an MQTT password.
    the_token = token_data['token']['encoded']

    print("\n\nYou will need to know your device_id to use MQTT.\n")
    print("Your device id is: \n" + token_data['token']['unencoded']['bot'] + "\n")
    print("The MQTT Host is: \n" + token_data['token']['unencoded']['mqtt'] + "\n")

    print("The token is: \n" + the_token)

    with open(config_path) as f:
        cfg = json.load(f)
        cfg['device_id'] = token_data['token']['unencoded']['bot']
        cfg['broker_url'] = token_data['token']['unencoded']['mqtt']
        cfg['token'] = the_token

    with open(config_path, 'w') as json_file:
        json.dump(cfg, json_file)
