# Pythonista API Client

## Installation

There's a package on [PyPI](https://pypi.org) just type:
```shell
pip install pythonista_api_client
```

### Desktop

To test your installation you can try one of the examples:
```shell
python examples/konektom.py
```

### iOS

Before you are able to install the package from PyPI, you have to install
[StaSh](https://github.com/ywangd/stash) a shell for pythonista.

## Api
To create an api client just inherit from BaseClient which will
handle authentication and settings for you. Requests should be
done by importing requests from api client which will then behave
like the usual requests module.

Depending on which platform your script will be run one of following
methods will be called:

- python_main (normal python)
- pythonista_main (started with pythonista play button)
- appex_main (invoked via share sheet)

### Token Authentication
If you wnat to use token authentication you need to set obtain_token_endpoint.

### JWT Authentication
For JWT Authentication obtain_jwt_endpoint and refresh_jwt_endpoint have to
be set.

### Example with token authentictaion
Here's a minimal example which should work with token and jwt authentication:

```python
from urllib.parse import urljoin

from api_client import requests
from api_client import BaseClient


class Bookmark(BaseClient):
    obtain_jwt_endpoint = 'api/auth/token/obtain/'
    refresh_jwt_endpoint = 'api/auth/token/refresh/'
    obtain_token_endpoint = '/api/api-token-auth/'

    bookmarks_endpoint = 'api/v1/bookmarks/'

    def list_bookmarks(self):
        list_url = urljoin(self.base_url, self.bookmarks_endpoint)
        return requests.get(list_url, auth=self.auth).json()

    def python_main(self):
        print('running in normal python')
        print(self.list_bookmarks())

    def pythonista_main(self):
        print('Running in Pythonista app, using test data...\n')
        print(self.list_bookmarks())

    def appex_main(self):
        print('running in share sheet')
        print(self.list_bookmarks())


def main():
    Bookmark(auth_method='token').main()

if __name__ == '__main__':
    main()
```
