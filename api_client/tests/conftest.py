import os
import pytest

from urllib.parse import urljoin

from ..client import BaseClient
from ..settings import BaseSettings

from .. import api as requests


class TestSettings(BaseSettings):
    def get_user_input(self):
        print('get user input..')
        return 'foo', 'bar', 'baz'


class FakeClient(BaseClient):
    obtain_jwtendpoint = 'api/auth/token/obtain/'
    refresh_jwt_endpoint = 'api/auth/token/refresh/'

    obtain_token_endpoint = '/api/api-token-auth/'
    resource_endpoint = 'api/v1/bookmarks/'

    def list_resource(self):
        list_url = urljoin(self.base_url, self.resource_endpoint)
        return requests.get(list_url, auth=self.auth).json()


@pytest.fixture
def settings_path():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(cur_dir, '.test.settings.json')


@pytest.fixture
def settings(settings_path):
    return TestSettings(config_path=settings_path)


@pytest.fixture
def client():
    client = FakeClient(auth_method='token')
    # settings = FakeSettings(client)
    return client
