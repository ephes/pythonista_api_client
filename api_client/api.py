import requests

from urllib.parse import urljoin

from .settings import Settings


class BaseApiAuth(requests.auth.AuthBase):
    def __init__(self):
        self.settings = Settings()


class JWTAuth(BaseApiAuth):
    def get_auth_token(self):
        token = self.get_auth_token_plain(
            self.settings.base_url, self.settings.username,
            self.settings.password)
        self.settings.set_token(token)

    def refresh_access_token(self):
        base_url = self.settings.base_url
        refresh_url = urljoin(base_url, self.settings.refresh_endpoint)
        r = requests.post(refresh_url, json=self.settings.credentials)
        r.raise_for_status()
        credentials = self.settings.credentials
        credentials['access'] = r.json()['access']
        self.settings.credentials = credentials

    def handle_auth_exception(self, e):
        print('access token expired fetching new one')
        try:
            self.refresh_access_token()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print('fetchting new access token failed, fall back to user..')
                self.settings.fetch_data_from_user()
            else:
                raise e

    def __call__(self, r):
        r.headers['Authorization'] = \
            f'Bearer {self.settings.credentials["access"]}'
        return r


class TokenAuth(BaseApiAuth):
    def __call__(self, r):
        token = self.settings.credentials['token']
        r.headers['Authorization'] = f'Token {token}'
        return r

    def handle_auth_exception(self, e):
        print('token invalid fetching new one')
        self.settings.fetch_data_from_user()


def request(method, url, **kwargs):
    def make_request():
        r = session.request(method=method, url=url, **kwargs)
        r.raise_for_status()
        return r

    auth = kwargs['auth']
    with requests.Session() as session:
        try:
            return make_request()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                auth.handle_auth_exception(e)
                return make_request()
            else:
                raise e


def get(url, params=None, **kwargs):
    return request('get', url, params=params, **kwargs)


def post(url, data=None, json=None, **kwargs):
    return request('post', url, data=data, json=json, **kwargs)
