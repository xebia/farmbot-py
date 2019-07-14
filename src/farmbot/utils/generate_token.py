# Copied from https://github.com/FarmBot-Labs/FarmBot-Python-Examples/blob/master/token_generation_example.py

import logging
import json
import requests
from farmbot.config import FarmBotConfiguration
import farmbot.log

USER_EMAIL_KEY = 'user_email'
USER_PASSWORD_KEY = 'user_password'
TOKEN_URL = "https://my.farm.bot/api/tokens"

cfg = FarmBotConfiguration('./config.json')
farmbot.log.configure_logger(cfg)
logger = logging.getLogger(__name__)

# Get an API token using email / password.
# To generate the token, we POST JSON to `api/tokens`.
data = {'user': {'email': cfg[USER_EMAIL_KEY], 'password': cfg[USER_PASSWORD_KEY]}}
result = requests.post(TOKEN_URL,
                       data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
token_data = json.loads(result.text)

# ... response_body.token.encoded is the important part- you will use this as
# an MQTT password.
the_token = token_data['token']['encoded']

print("\n\nYou will need to know your device_id to use MQTT.\n")
print("Your device id is: \n" + token_data['token']['unencoded']['bot'] + "\n")
print("The MQTT Host is: \n" + token_data['token']['unencoded']['mqtt'] + "\n")
print("The token is: \n" + the_token)
