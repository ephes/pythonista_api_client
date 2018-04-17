try:
    import ui
    import appex
    import webbrowser
except ImportError:
    pass

import api as requests

from api import JWTAuth
from settings import settings
from urllib.parse import urljoin


class Bookmark:
    bookmarks_endpoint = 'api/v1/bookmarks/'

    def __init__(self, settings):
        self.settings = settings
        self.auth = JWTAuth(settings)
        self.base_url = settings.base_url

    def add_bookmark(self, url, title=''):
        add_url = urljoin(self.base_url, self.bookmarks_endpoint)
        payload = {
            'url': {'the_url': url},
            'title': title,
        }
        return requests.post(add_url, json=payload, auth=self.auth)

    def list_bookmarks(self):
        list_url = urljoin(self.base_url, self.bookmarks_endpoint)
        return requests.get(list_url, auth=self.auth).json()


def python_main():
    print('running in normal python')
    #print(settings.data)
    #print(bm.list_bookmarks())
    bm = Bookmark(settings)
    data = bm.add_bookmark('http://example.org', title='foobar').json()
    print(data)
    print(data['api_url'].replace('api/v1/', ''))


def pythonista_main():
    print('Running in Pythonista app, using test data...\n')
    print('settings...')
    settings.data = settings.get_data_from_user()
    bm = Bookmark(settings)
    data = bm.add_bookmark('example.org', title='foobar').json()
    detail_url = data['api_url'].replace('api/v1/', '')
    webbrowser.open(detail_url)


def appex_main():
    print('running in share sheet')
    url = appex.get_url()
    print(appex.get_urls())
    print(url)
    if url:
        print('Input URL: %s' % (url,))
        bm = Bookmark(settings)
        data = bm.add_bookmark(url, title='').json()
        detail_url = data['api_url'].replace('api/v1/', '')
        webbrowser.open(detail_url)
    else:
        print('No input URL found.')


def main():
    if not settings.ios:
        python_main()
    else:
        if not appex.is_running_extension():
            pythonista_main()
        else:
            appex_main()


if __name__ == '__main__':
    main()
