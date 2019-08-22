"""
Farmbot token generator.

Copied and adapted from https://github.com/FarmBot-Labs/FarmBot-Python-Examples/blob/master/token_generation_example.py
"""

import argparse
import json
from urllib.request import Request, urlopen

REQUEST_TOKEN_URL = "https://my.farm.bot/api/tokens"

OUTPUT_TEXT = f"""Farmbot Token Generator

Copy / Paste this information into your config.json:

  "broker_url": "{{1}}",
  "device_id": "{{0}}",
  "token": "{{2}}",
"""


def parse_command_line():
    parser = argparse.ArgumentParser(
        description="""Create token for the Farmbot MQTT API"""
    )
    parser.add_argument('username',
                        help="Farmbot account username. Is currently your email address.",
                        type=str)
    parser.add_argument('password',
                        help="Farmbot account password.",
                        type=str)
    return parser.parse_args()


def create_token(username, password):
    """Get an API token using username (email) / password."""
    data = {'user': {'email': username, 'password': password}}
    req = Request(REQUEST_TOKEN_URL, data=json.dumps(data).encode('UTF-8'), headers={'Content-Type': 'application/json'})
    with urlopen(req) as resp:
        token_data = json.loads(resp.read().decode("utf-8"))
    return token_data


def print_token_info(token_data):
    device_id = token_data['token']['unencoded']['bot']
    mqtt_host = token_data['token']['unencoded']['mqtt']
    encoded_token = token_data['token']['encoded']
    print(OUTPUT_TEXT.format(device_id, mqtt_host, encoded_token))


if __name__ == '__main__':
    args = parse_command_line()
    token = create_token(args.username, args.password)
    print_token_info(token)
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
