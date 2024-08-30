from datetime import datetime
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
import pytz
from sideshow.apps.tokens.graphapi import get_token_data, get_token_day_data, get_token_hour_data
from sideshow.apps.tokens.models import TokenAddresses, Token, TokenHourData
import json
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def decimal_to_float(data):
    if isinstance(data, list):
        return [decimal_to_float(item) for item in data]
    elif isinstance(data, dict):
        return {key: decimal_to_float(value) for key, value in data.items()}
    elif isinstance(data, Decimal):
        return float(data)
    return data

def run():
    logging.info("Getting tokens...")
    for address, name in TokenAddresses.choices:
        token_data = get_token_data(address)
        token = Token.upsert_api_data(token_data)
    
    logging.info("Backfilling token hour data for the past 7 days...")
    from datetime import timedelta

    start_date = datetime.now().date() - timedelta(days=7)
    end_date = datetime.now().date()

    for token in Token.objects.all():
        current_date = start_date
        while current_date <= end_date:
            token_day_data = get_token_day_data(token.address, current_date)
            for hour_data in token_day_data:
                TokenHourData.upsert_api_data(token, hour_data)
            current_date += timedelta(days=1)

    if os.getenv('KEEP_POLLING'):
        while True:
            current_time = datetime.now(pytz.utc).replace(minute=0, second=0, microsecond=0)
            start_timestamp = int((current_time - timedelta(hours=1)).timestamp())
            end_timestamp = int(current_time.timestamp())
            logging.info(f"Polling latest hour data for {current_time}...")
            for token in Token.objects.all():
                token_hour_data = get_token_hour_data(token.address, start_timestamp, end_timestamp)
                for hour_data in token_hour_data:
                    TokenHourData.upsert_api_data(token, hour_data)
            
            time.sleep(600)  # Sleep for 10 minutes
    else:
        for token in Token.objects.all():
            chart_data = token.get_chart_data(4)
            chart_data = decimal_to_float(chart_data)
            logging.info(json.dumps(chart_data, indent=2, cls=DjangoJSONEncoder))