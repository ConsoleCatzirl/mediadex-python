from arango import ArangoClient

from mediadex.arangodb import Client


def test_arango(mocker, fake_config, fake_item):
    fake_client = Client(fake_config.settings["arangodb"])

    mock_upstream = mocker.MagicMock(autospec=ArangoClient)
    mocker.patch("arango.ArangoClient.__new__", return_value=mock_upstream)

    fake_client.index(fake_item)
