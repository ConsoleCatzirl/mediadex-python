from arango import ArangoClient

from mediadex.arangodb import Client
from mediadex.item import Item, Family


def test_arango(mocker, fake_config):
    fake_client = Client(fake_config.settings["arangodb"])

    mock_upstream = mocker.MagicMock(spec=ArangoClient)
    mocker.patch("arango.ArangoClient.__new__", return_value=mock_upstream)

    fake_item = Item(Family.MOVIES, "fake", "fake", "fake")
    fake_item._fingerprint = "fake"
    fake_item._mediainfo = "fake"

    fake_client.index(fake_item)
