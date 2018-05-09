import requests

from urllib.parse import urljoin

from .settings import Settings


class BaseApiAuth(requests.auth.AuthBase):
    def __init__(self):
        self.settings = Settings()

    def parse_exception(self, e):
        pass


class JWTAuth(BaseApiAuth):
    def get_auth_token(self):
        token = self.get_auth_token_plain(
            self.settings.base_url, self.settings.username,
            self.settings.password)
        self.settings.set_token(token)

    def refresh_access_token(self):
        token = self.settings.token
        base_url = self.settings.base_url
        refresh_url = urljoin(base_url, self.settings.refresh_endpoint)
        r = requests.post(refresh_url, json=token)
        r.raise_for_status()
        self.settings.set_access_token(r.json()['access'])

    def handle_auth_exception(self, e):
        print('access token expired fetching new one')
        self.refresh_access_token()

#            print('access token expired fetching new one')
#            auth.refresh_access_token()
#            try:
#                return make_request()
#            except requests.exceptions.HTTPError as e:
#                print('refresh token expired fetching new one')
#                auth.get_auth_token()
#                return make_request()

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.settings.access_token}'
        return r


class TokenAuth(BaseApiAuth):
    def __call__(self, r):
        token = self.settings.credentials['token']
        r.headers['Authorization'] = f'Token {token}'
        return r

    def handle_auth_exception(self, e):
        print('token invalid fetching new one')
        self.settings.fetch_data_from_user()
        print(e)


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
