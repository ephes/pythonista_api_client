import requests

from urllib.parse import urljoin


class JWTAuth(requests.auth.AuthBase):
    def __init__(self, settings):
        self.settings = settings

    def get_auth_token_plain(self, base_url, username, password):
        obtain_url = urljoin(base_url, self.settings.obtain_endpoint)
        payload = {'username': username, 'password': password}
        print(obtain_url)
        r = requests.post(obtain_url, json=payload)
        print(r.status_code)
        print(r.json())
        r.raise_for_status()
        return r.json()

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

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.settings.access_token}'
        return r


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
            print('access token expired fetching new one')
            auth.refresh_access_token()
            try:
                return make_request()
            except requests.exceptions.HTTPError as e:
                print('refresh token expired fetching new one')
                auth.get_auth_token()
                return make_request()


def get(url, params=None, **kwargs):
    return request('get', url, params=params, **kwargs)


def post(url, data=None, json=None, **kwargs):
    return request('post', url, data=data, json=json, **kwargs)
