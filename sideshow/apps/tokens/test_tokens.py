
from datetime import datetime
from decimal import Decimal

import pytz
from sideshow.apps.tokens.models import Token, TokenHourData


def test_token_data_loaded(project_fixture_common):
    assert Token.objects.count() == 3

def test_token_hour_data_correct(project_fixture_common):
    token = Token.objects.get(symbol='WBTC')
    assert TokenHourData.objects.filter(token=token).count() == 24
    datapoint = TokenHourData.objects.get(token=token, timestamp=datetime.fromtimestamp(1724803200, pytz.utc))
    assert int(datapoint.priceUSD) == 59192

def test_chart_data_correct(project_fixture_common):
    token = Token.objects.get(symbol='WBTC')
    price_data = token.get_chart_data(4)[4]
    assert len(price_data) == 6
    # Test hardcoded values based on fixtures/token_hour_data_2024-08-28.json
    assert int(price_data[0][2]) == 59338
    assert int(price_data[1][2]) == 59009
    assert int(price_data[2][2]) == 59773
    assert int(price_data[3][2]) == 59362
    assert int(price_data[4][2]) == 58993
    assert int(price_data[5][2]) == 59132

def test_chart_data_empty_correct(project_fixture_common):
    token = Token.objects.get(symbol='GNO')
    price_data = token.get_chart_data(4, datetime.fromtimestamp(1724803200, pytz.utc))[4]
    assert len(price_data) == 6
    assert int(price_data[0][2]) == 0, "datapoints with no data should be 0"
    assert int(price_data[1][2]) == 154
    assert int(price_data[2][2]) == 0, "datapoints with no data should be 0"
    assert int(price_data[3][2]) == 157
    assert int(price_data[4][2]) == 0, "datapoints with no data should be 0"
    assert int(price_data[5][2]) == 157