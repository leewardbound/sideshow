from dataclasses import dataclass
import json
from sideshow.apps.users.models import User
from sideshow.apps.users.factories import UserFactory
from sideshow.apps.tokens.models import Token, TokenHourData
import django.conf
import pytest

@pytest.fixture
def strong_pass():
    # Test password is very strong
    return "DevAuth1234!!"


@dataclass
class ProjectFixture:
    settings: django.conf.Settings
    user: User


@pytest.fixture
def project_fixture_common(db, settings):
    user = UserFactory.create()

    with open('fixtures/token_data.json') as f:
        token_data = json.load(f)
        for token in token_data.values():
            Token.upsert_api_data(token)
    
    with open('fixtures/token_hour_data_2024-08-28.json') as f:
        token_hour_data = json.load(f)
        for token in Token.objects.all():
            for hour_data in token_hour_data[token.symbol]:
                TokenHourData.upsert_api_data(token, hour_data)


    return ProjectFixture(settings=settings, user=user)

