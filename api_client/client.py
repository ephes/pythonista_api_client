try:
    import appex
    IOS = True
except ImportError:
    IOS = False

from .api import JWTAuth
from .api import TokenAuth
from .settings import Settings


class BaseClient:
    def __init__(self, auth_method='token'):
        self.auth_method = auth_method
        self.settings = Settings()
        if not hasattr(self.settings, 'obtain_endpoint'):
            self.settings.obtain_endpoint = self.obtain_endpoint
        if auth_method == 'jwt':
            self.settings.refresh_endpoint = self.refresh_jwt_endpoint
        self.settings.check_is_complete()
        self.base_url = self.settings.base_url
        self.auth = JWTAuth() if auth_method == 'jwt' else TokenAuth()

    def get_obtain_endpoint(self, auth_method):
        if auth_method == 'jwt':
            return

    @property
    def obtain_endpoint(self):
        if self.auth_method == 'jwt':
            return self.obtain_jwt_endpoint
        else:
            return self.obtain_token_endpoint

    def main(self):
        if not self.settings.ios:
            self.python_main()
        else:
            if not appex.is_running_extension():
                self.pythonista_main()
            else:
                self.appex_main()
                appex.finish()
