# Pythonista API Client

## Installation

You can use the checked out repository directly. There's no package at the moment.

### Desktop

```shell
pip install -r requirements.txt
python client.py
```

### iOS

If you are using pythonista 3, there's an iCloud integration. If you checked out the repository in the pythonista 3 icloud directory, all changes should be transferred to your iOS-device immediately.

```shell
cd "${HOME}/Library/Mobile Documents/iCloud~com~omz-software~Pythonista3/Documents"
git clone https://github.com/ephes/pythonista_api_client
```

If you are using the client_api as an app extension, you have to import it first from the icloud directory to your local devices file system. And you have to import it every time you change something.
