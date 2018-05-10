try:
    import ui
    import appex
    import dialogs
    import webbrowser
except ImportError:
    pass

from urllib.parse import urljoin

from api_client import requests
from api_client import BaseClient


class Bookmark(BaseClient):
    obtain_jwt_endpoint = 'api/auth/token/obtain/'
    refresh_jwt_endpoint = 'api/auth/token/refresh/'

    obtain_token_endpoint = '/api/api-token-auth/'
    bookmarks_endpoint = 'api/v1/bookmarks/'

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


def main():
    Bookmark(auth_method='token').main()

if __name__ == '__main__':
    main()
