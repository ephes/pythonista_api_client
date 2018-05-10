import pytest
import requests

from unittest.mock import patch


def test_jwt_auth_wrong_try_refresh(
        client, settings, mocked_jwt_auth, not_auth_response):
    """Assert that on authentication error the refresh_access_token method
       of JWTAuth gets called."""
    client.settings = settings
    client.auth = mocked_jwt_auth
    assert not client.auth.refresh_access_token_called

    args = [requests.Session, 'request']
    kwargs = {'return_value': not_auth_response}
    with patch.object(*args, **kwargs):
        with pytest.raises(requests.exceptions.HTTPError):
            client.list_resource()
    assert client.auth.refresh_access_token_called
