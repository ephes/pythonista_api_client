try:
    import dialogs
    IOS = True
except ImportError as e:
    IOS = False
    import getpass

import os
import json
import requests

from collections import UserDict
from urllib.parse import urljoin


CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    '.settings.json')


class PersistentDict(UserDict):
    required_keys = ['username', 'base_url', 'credentials', 'obtain_endpoint']

    def __init__(self, filename, initialdata=None):
        self.filename = filename
        if initialdata is not None:
            self.write_data_to_file(initialdata)
        self.data = self.get_data_from_file()

    def get_data_from_file(self):
        try:
            with open(self.filename) as f:
                return json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            return {}

    def write_data_to_file(self, data):
        print(f'write data to file: {self.filename}')
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def file_sync(self):
        self.write_data_to_file(self.data)
        self.data = self.get_data_from_file()

    @property
    def is_complete(self):
        valid = True
        for key in self.required_keys:
            if key not in self.data:
                valid = False
        return valid

    def __setitem__(self, key, item):
        super().__setitem__(key, item)
        self.file_sync()


class BaseSettings:
    data = None

    def __new__(cls, config_path=None):
        if cls.data is None:
            if config_path is not None:
                cls.data = PersistentDict(config_path)
            else:
                cls.data = PersistentDict(CONFIG_PATH)
        return super().__new__(cls)

    def check_is_complete(self):
        if not self.data.is_complete:
            self.fetch_data_from_user()

    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError as e:
            raise AttributeError(f'BaseSettings.data has no key "{name}"')

    def __setattr__(self, name, value):
        if name in self.data or not hasattr(self, name):
            self.data[name] = value
        else:
            super().__setattr__(name, value)

    def get_credentials(self, password):
        obtain_url = urljoin(self.base_url, self.obtain_endpoint)
        payload = {'username': self.username, 'password': password}
        r = requests.post(obtain_url, json=payload)
        r.raise_for_status()
        return r.json()

    def fetch_data_from_user(self):
        done = False
        while not done:
            self.username, password, self.base_url = self.get_user_input()
            try:
                credentials = self.get_credentials(password)
                done = True
            except requests.exceptions.HTTPError as e:
                print(e)
                print('some input was not correct, try again..')
        self.credentials = credentials


class PythonSettings(BaseSettings):
    ios = False

    def get_user_input(self):
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        base_url = input('Base URL: ')
        return username, password, base_url


class IosSettings(BaseSettings):
    ios = True

    def get_user_input(self):
        fields = [{
            'key': 'username', 'type': 'text', 'title': 'Username',
            'value': self.data.get('username', '')
        }, {
            'key': 'password', 'type': 'password', 'title': 'Password',
            'value': self.data.get('password', ''),
        }, {
            'key': 'base_url', 'type': 'text', 'title': 'Base URL',
            'value': self.data.get('base_url', '')
        }]
        data = dialogs.form_dialog(title='Settings', fields=fields)
        print(data)
        return data['username'], data['password'], data['base_url']


if IOS:
    Settings = IosSettings
else:
    Settings = PythonSettings
