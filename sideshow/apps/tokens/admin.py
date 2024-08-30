from .models import Token, TokenHourData
from sideshow.utils.admin import register
from django.contrib import admin

@register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'totalSupply', 'volumeUSD', 'decimals')
    search_fields = ('name', 'symbol')

@register(TokenHourData)
class TokenHourDataAdmin(admin.ModelAdmin):
    list_display = ('token', 'open', 'close', 'high', 'low', 'priceUSD', 'timestamp')
    search_fields = ('token__name', 'token__symbol')
    list_filter = ('token', 'timestamp')
