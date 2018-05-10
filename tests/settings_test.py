import os
import json


def test_settings_assign_write(settings):
    """Test wether an assignment leads to config file being written."""
    config_path = settings.data.filename
    try:
        os.unlink(config_path)
    except FileNotFoundError as e:
        pass
    settings.foo = 'bar'
    with open(config_path) as f:
        data = json.load(f)
    assert data['foo'] == 'bar'
