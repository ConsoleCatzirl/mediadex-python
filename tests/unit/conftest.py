from io import BytesIO

from mediadex.config import Config

import pytest


@pytest.fixture
def fake_config():
    conf = {
        "paths": {
            "movies": [
                "foo",
            ],
        },
        "arangodb": {
            "hosts": [
                "http://localhost:8529",
            ],
        },
        "opensearch": {
            "hosts": [
                "https://localhost:9200",
            ],
        },
    }
    return Config(conf)


@pytest.fixture
def fake_file():
    io = BytesIO(b'12345')
    return io


@pytest.fixture
def fake_file_hash():
    return "0fa76955abfa9dafd83facca8343a92aa09497f98101086611b0bfa95dbc0dcc661d62e9568a5a032ba81960f3e55d4a"
