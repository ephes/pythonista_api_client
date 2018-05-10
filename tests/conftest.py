import os
import pytest
import requests

from urllib.parse import urljoin

from api_client import BaseClient
from api_client import BaseSettings

from api_client import api


class MockedSettings(BaseSettings):
    fetch_data_from_user_called = False
    credentials = {'token': 'foobar'}
    base_url = 'http://localhost:8000'

    def get_credentials(self, password):
        raise 'Foobar'

    def get_user_input(self):
        print('get user input..')
        return 'username', 'password', self.base_url

    def fetch_data_from_user(self):
        self.fetch_data_from_user_called = True


class MockedTokenAuth(api.TokenAuth):
    handle_auth_exception_called = False

    def handle_auth_exception(self, e):
        self.handle_auth_exception_called = True


class MockedClient(BaseClient):
    obtain_jwtendpoint = 'api/auth/token/obtain/'
    refresh_jwt_endpoint = 'api/auth/token/refresh/'

    obtain_token_endpoint = '/api/api-token-auth/'
    resource_endpoint = 'api/v1/bookmarks/'

    def list_resource(self):
        list_url = urljoin(self.base_url, self.resource_endpoint)
        return api.get(list_url, auth=self.auth).json()


class MockedResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text
        self.content = text.encode('utf-8')

    def raise_for_status(self):
        http_error_msg = ''
        if 400 <= self.status_code < 500:
            http_error_msg = \
                f'{self.status_code} mocked Client Error: {self.text}'
        elif 500 <= self.status_code < 600:
            http_error_msg = \
                f'{self.status_code} mocked Server Error: {self.text}'
        raise requests.exceptions.HTTPError(
            http_error_msg, response=self)


@pytest.fixture
def settings_path():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(cur_dir, '.test.settings.json')


@pytest.fixture
def settings(settings_path):
    return MockedSettings(config_path=settings_path)


@pytest.fixture
def mocked_token_auth():
    return MockedTokenAuth()


@pytest.fixture
def client():
    return MockedClient(auth_method='token')
    # settings.obtain_endpoint = client.obtain_endpoint
    # client.settings = settings
    # client.auth.settings = settings


@pytest.fixture
def not_auth_response():
    return MockedResponse(401, 'authentication error')
