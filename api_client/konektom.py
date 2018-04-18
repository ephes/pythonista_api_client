try:
    import ui
    import appex
    import dialogs
    import webbrowser
    IOS = True
except ImportError:
    IOS = False

from urllib.parse import urljoin

from . import api as requests

from .api import JWTAuth
from .settings import IosSettings
from .settings import PythonSettings


class BaseClient:
    def main(self):
        if not self.settings.ios:
            self.python_main()
        else:
            if not appex.is_running_extension():
                self.pythonista_main()
            else:
                self.appex_main()
                appex.finish()


class Bookmark(BaseClient):
    obtain_endpoint = 'api/auth/token/obtain/'
    refresh_endpoint = 'api/auth/token/refresh/'
    bookmarks_endpoint = 'api/v1/bookmarks/'

    def __init__(self):
        self.settings = IosSettings(self) if IOS else PythonSettings(self)
        self.settings.ios = IOS
        self.base_url = self.settings.base_url
        self.auth = self.get_auth(self.settings, self.base_url)

    def get_auth(self, settings, base_url):
        settings.obtain_endpoint = urljoin(
            base_url, self.obtain_endpoint)
        settings.refresh_endpoint = urljoin(
            base_url, self.refresh_endpoint)
        return JWTAuth(settings)

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

    def show_bookmark_list_table_view(self):
        bookmark_list = self.list_bookmarks()
        # print(bookmark_list)
        items = [i['url']['the_url'] for i in bookmark_list['results']]
        data_source = ui.ListDataSource(items=items)
        btv = ui.TableView()
        btv.data_source = data_source
        btv.tableview_title_for_header = lambda x, y, z: 'Bookmark List'
        btv.present()

    def python_main(self):
        print('running in normal python')
        # print(settings.data)
        print(self.list_bookmarks())
        # data = self.add_bookmark('http://example.org', title='foobar').json()
        # print(data)
        # print(data['api_url'].replace('api/v1/', ''))

    def pythonista_main(self):
        print('Running in Pythonista app, using test data...\n')
        print('settings...')
        action = dialogs.list_dialog(
            title='Konektom Bookmark Menu',
            items=['list bookmarks', 'settings', 'quit'])
        if action == 'settings':
            self.settings.fetch_data_from_user()
        elif action == 'list bookmarks':
            self.show_bookmark_list_table_view()
        elif action == 'quit':
            print('quit')

    def appex_main(self):
        print('running in share sheet')
        url = appex.get_url()
        if url:
            print('Input URL: %s' % (url,))
            data = self.add_bookmark(url, title='').json()
            detail_url = data['api_url'].replace('api/v1/', '')
            webbrowser.open(detail_url)
        else:
            print('No input URL found.')
