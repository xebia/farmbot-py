# Copied from https://github.com/FarmBot-Labs/FarmBot-Python-Examples/blob/master/token_generation_example.py

import json
import requests

# Get an API token using email / password.
data = {'user': {'email': 'fvanwijk@xebia.com', 'password': '9Bi5*&jd3fzY'}}

result = requests.post("https://my.farm.bot/api/tokens",
                       data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})

# To generate the token, we POST JSON to `api/tokens`.
token_data = json.loads(result.text)

# ... response_body.token.encoded is the important part- you will use this as
# an MQTT password.
the_token = token_data['token']['encoded']

print("\n\nYou will need to know your device_id to use MQTT.\n")
print("Your device id is: \n" + token_data['token']['unencoded']['bot'] + "\n")
print("The MQTT Host is: \n" + token_data['token']['unencoded']['mqtt'] + "\n")
# You can copy/paste this data and move on to `subscribe_example.py`.
print("The token is: \n" + the_token)