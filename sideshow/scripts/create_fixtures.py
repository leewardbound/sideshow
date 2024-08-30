
import json
from sideshow.apps.tokens.graphapi import get_token_data, get_token_day_data
from sideshow.apps.tokens.models import TokenAddresses


def save_token_data():
    with open('fixtures/token_data.json', 'w') as f:
        data = {
            name.upper(): get_token_data(address) for address, name in TokenAddresses.choices
        }
        print(data)
        f.write(json.dumps(data, indent=4))

def save_token_hour_data():
    day = '2024-08-28'
    with open(f'fixtures/token_hour_data_{day}.json', 'w') as f:
        data = {
            name.upper(): get_token_day_data(address, day) for address, name in TokenAddresses.choices
        }
        print(data)
        f.write(json.dumps(data, indent=4))

def run():
    save_token_data()
    save_token_hour_data()
        