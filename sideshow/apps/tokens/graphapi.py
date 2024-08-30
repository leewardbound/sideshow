from datetime import date, datetime
import os

import requests
GRAPH_API_KEY = os.getenv('GRAPH_API_KEY')
GRAPH_URL = f'https://gateway.thegraph.com/api/{GRAPH_API_KEY}/subgraphs/id/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV'

def get_token_data(token_address: str):
    query = f"""
    {{
        token(id: "{token_address}") {{
            id
            name
            symbol
            totalSupply
            volumeUSD
            decimals
        }}
    }}
    """
    response = requests.post(GRAPH_URL, json={'query': query})
    return response.json()['data']['token']


def get_token_hour_data(token_address: str, start_timestamp: int, end_timestamp: int):
    query = f"""
    {{
        tokenHourDatas(where: {{token: "{token_address}", periodStartUnix_gte: {start_timestamp}, periodStartUnix_lte: {end_timestamp}}}) {{
            open
            close
            high
            low
            priceUSD
            periodStartUnix
        }}
    }}
    """
    response = requests.post(GRAPH_URL, json={'query': query})
    return response.json()['data']['tokenHourDatas']

def get_token_day_data(token_address: str, day: date | str):
    if isinstance(day, str):
        day = datetime.strptime(day, '%Y-%m-%d').date()
    start_timestamp = int(day.strftime('%s'))
    end_timestamp = start_timestamp + 24 * 60 * 60
    return get_token_hour_data(token_address, start_timestamp, end_timestamp)