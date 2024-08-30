import asyncio
from datetime import datetime, timedelta
from typing import AsyncIterator
from fastapi import Depends
from mountaineer import RenderBase, passthrough, sideeffect
from django.utils import timezone
from asgiref.sync import sync_to_async

from django.db.models import Q
from django_mountaineer.controllers import PageController
from sideshow.utils.auth import AuthDependencies, UserProfileOutput

from pydantic import ConfigDict, BaseModel
from djantic import ModelSchema
from sideshow.apps.tokens import models

class ChartData(BaseModel):
    open: list[tuple[str, str, float]]
    close: list[tuple[str, str, float]]
    high: list[tuple[str, str, float]]
    low: list[tuple[str, str, float]]
    priceUSD: list[tuple[str, str, float]]

class TokenOutput(ModelSchema):
    model_config = ConfigDict(model=models.Token, include=["id", "name", "symbol", "address", "volumeUSD", "totalSupply", "decimals"])
    address: str
    name: str
    symbol: str
    chartData: ChartData | None

class HomeRender(RenderBase):
    user: UserProfileOutput | None
    tokens: list[TokenOutput]

# Need to wrap render in sync_to_async
class HomeController(PageController()):
    def render( self, user: UserProfileOutput | None = Depends(AuthDependencies.get_user) ) -> HomeRender:
        tokens = []
        for token in models.Token.objects.all():
            chart_data = token.get_chart_data(1, timezone.now() - timedelta(days=7))
            tokens.append(TokenOutput(
                address=token.address,
                name=token.name,
                symbol=token.symbol,
                volumeUSD=token.volumeUSD,
                totalSupply=token.totalSupply,
                decimals=token.decimals,
                chartData=ChartData(
                    open=chart_data[0],
                    close=chart_data[1],
                    high=chart_data[2],
                    low=chart_data[3],
                    priceUSD=chart_data[4],
                )
            ))

        return HomeRender(
            user=user,
            tokens=tokens
        )

    @passthrough
    async def get_chart_data(self, token_address_or_name: str, time_unit_in_hours: int) -> ChartData:
        start_date = timezone.now() - timedelta(days=7)
        token = await models.Token.objects.filter(
            Q(address__iexact=token_address_or_name) |
            Q(name__iexact=token_address_or_name) |
            Q(symbol__iexact=token_address_or_name)
        ).afirst()
        
        if not token:
            raise models.Token.DoesNotExist("Token not found")
        chart_data = await sync_to_async(token.get_chart_data)(time_unit_in_hours, start_date)
        return ChartData(
            open=chart_data[0],
            close=chart_data[1],
            high=chart_data[2],
            low=chart_data[3],
            priceUSD=chart_data[4],
        )