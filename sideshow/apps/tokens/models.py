from datetime import datetime, timedelta
from decimal import Decimal
from django.db import models
import pytz

class TokenAddresses(models.TextChoices):
    WBTC = '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599'
    SHIB = '0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce'
    GNO = '0x6810e776880c02933d47db1b9fc05908e5386b96'


class Token(models.Model):
    address = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=50, db_index=True)
    totalSupply = models.DecimalField(max_digits=30, decimal_places=10)
    volumeUSD = models.DecimalField(max_digits=30, decimal_places=10)
    decimals = models.IntegerField()

    @staticmethod
    def ADDRESSES():
        return TokenAddresses

    @classmethod
    def upsert_api_data(cls, data):
        token, _ = cls.objects.update_or_create(address=data['id'], defaults={
            'name': data['name'],
            'symbol': data['symbol'],
            'totalSupply': data['totalSupply'],
            'volumeUSD': data['volumeUSD'],
            'decimals': data['decimals']
        })
        return token
    
    def get_chart_data(self, time_unit_in_hours: int, start_date: datetime | None = None, end_date: datetime | None = None):
        from dateutil.rrule import rrule, HOURLY

        # Prepare the 3D array
        chart_data = {
            'open': [],
            'close': [],
            'high': [],
            'low': [],
            'priceUSD': []
        }

        # Get the earliest and latest timestamps for the token
        if start_date is None:
            start_date = TokenHourData.objects.filter(token=self).order_by('timestamp').first().timestamp
        if end_date is None:
            end_date = TokenHourData.objects.filter(token=self).order_by('-timestamp').first().timestamp
        
        start_date = start_date.replace(minute=0, second=0, microsecond=0)
        end_date = end_date.replace(minute=0, second=0, microsecond=0)

        # Iterate over time windows
        for dt in rrule(HOURLY, dtstart=start_date, until=end_date, interval=time_unit_in_hours):
            start_time = dt
            end_time = dt + timedelta(hours=time_unit_in_hours)
            time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S')

            # Query for the data within the current time window
            window_data = TokenHourData.objects.filter(
                token=self,
                timestamp__gte=start_time,
                timestamp__lt=end_time
            ).order_by('timestamp')

            if window_data.exists():
                open_price = window_data.first().open
                close_price = window_data.last().close
                high_price = window_data.aggregate(models.Max('high'))['high__max']
                low_price = window_data.aggregate(models.Min('low'))['low__min']
                avg_price = window_data.aggregate(models.Avg('priceUSD'))['priceUSD__avg']
            else:
                open_price = close_price = high_price = low_price = avg_price = 0

            chart_data['open'].append([time_str, 'open', open_price])
            chart_data['close'].append([time_str, 'close', close_price])
            chart_data['high'].append([time_str, 'high', high_price])
            chart_data['low'].append([time_str, 'low', low_price])
            chart_data['priceUSD'].append([time_str, 'priceUSD', avg_price])

        return [
            chart_data['open'],
            chart_data['close'],
            chart_data['high'],
            chart_data['low'],
            chart_data['priceUSD']
        ]

    def __str__(self):
        return self.name

class TokenHourData(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    open = models.DecimalField(max_digits=30, decimal_places=10)
    close = models.DecimalField(max_digits=30, decimal_places=10)
    high = models.DecimalField(max_digits=30, decimal_places=10)
    low = models.DecimalField(max_digits=30, decimal_places=10)
    priceUSD = models.DecimalField(max_digits=30, decimal_places=10)
    timestamp = models.DateTimeField()

    @classmethod
    def upsert_api_data(cls, token, data):
        timestamp = datetime.fromtimestamp(data['periodStartUnix'], tz=pytz.utc)
        token_hour_data, _ = cls.objects.update_or_create(token=token, timestamp=timestamp, defaults={
            'open': Decimal(data['open']),
            'close': Decimal(data['close']),
            'high': Decimal(data['high']),
            'low': Decimal(data['low']),
            'priceUSD': Decimal(data['priceUSD'])
        })
        return token_hour_data
    def __str__(self):
        return f"{self.token.name} - {self.timestamp}"
