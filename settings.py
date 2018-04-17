try:
    import ui
    import appex
    import dialogs
    IOS = True
except ImportError as e:
    print(e)
    IOS = False
    import getpass

import os
import json
import requests

from api import JWTAuth
from collections import UserDict


class PersistentDict(UserDict):
    def __init__(self, filename, initialdata=None):
        self.filename = filename
        if initialdata is not None:
            self.write_data_to_file(initialdata)
        initialdata = self.get_data_from_file()
        super().__init__(initialdata)

    def get_data_from_file(self):
        try:
            with open(self.filename) as f:
                return json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            return {}

    def write_data_to_file(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def file_sync(self):
        self.write_data_to_file(self.data)
        self.data = self.get_data_from_file()

    @property
    def is_valid(self):
        valid = True
        for key in ['username', 'password', 'base_url', 'token']:
            if key not in self.data:
                valid = False
        return valid

    def __setitem__(self, key, item):
        super().__setitem__(key, item)
        self.file_sync()


class BaseSettings:
    def __init__(self, ios=IOS, filename='.settings.json'):
        self.ios = ios
        self.data = PersistentDict(filename)
        if not self.data.is_valid:
            initialdata = self.get_data_from_user()
            self.data  = PersistentDict(filename, initialdata=initialdata)

    @property
    def base_url(self):
        return self.data['base_url']

    @property
    def token(self):
        return self.data['token']

    @property
    def access_token(self):
        return self.token['access']

    @property
    def refresh_token(self):
        return self.token['refresh']

    @property
    def username(self):
        return self.data['username']

    @property
    def password(self):
        return self.data['password']

    def set_token(self, token):
        self.data['token'] = token

    def set_access_token(self, access_token):
        self.data['token']['access'] = access_token

    def get_data_from_user(self):
        done = False
        while not done:
            username, password, base_url = self.get_user_input()
            try:
                auth_token = JWTAuth(None).get_auth_token_plain(
                    base_url, username, password)
                done = True
            except requests.exceptions.HTTPError as e:
                print('some input was not correct, try again..')
        data = {
            'base_url': base_url,
            'username': username,
            'password': password,
            'token': auth_token
        }
        return data


class PythonSettings(BaseSettings):
    def get_user_input(self):
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        base_url = input('Base URL: ')
        return username, password, base_url


class IosSettings(BaseSettings):
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
        return data['username'], data['password'], data['base_url']


settings = IosSettings(ios=True) if IOS else PythonSettings(ios=False)
