import pytest
import requests

from unittest.mock import patch


def test_token_auth_wrong_token(
        client, settings, mocked_token_auth, not_auth_response):
    """Assert that on authentication error the handle_auth_exception method
       of TokenAuth gets called."""
    client.settings = settings
    client.auth = mocked_token_auth
    assert not client.auth.handle_auth_exception_called

    args = [requests.Session, 'request']
    kwargs = {'return_value': not_auth_response}
    with patch.object(*args, **kwargs):
        with pytest.raises(requests.exceptions.HTTPError):
            client.list_resource()
    assert client.auth.handle_auth_exception_called


def test_token_auth_wrong_token_user_input(
        client, settings, not_auth_response):
    """Assert that on authentication error the handle_auth_exception
       method calls fetch_data_from_user from settings."""
    client.settings = settings
    client.auth.settings = settings
    assert not settings.fetch_data_from_user_called

    args = [requests.Session, 'request']
    kwargs = {'return_value': not_auth_response}
    with patch.object(*args, **kwargs):
        with pytest.raises(requests.exceptions.HTTPError):
            client.list_resource()
    assert settings.fetch_data_from_user_called
