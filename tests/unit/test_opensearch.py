from opensearchpy import OpenSearch

from mediadex.opensearch import Client


def test_opensearch(mocker, fake_config, fake_item):
    fake_client = Client(fake_config.settings["opensearch"])

    mock_upstream = mocker.MagicMock(autospec=OpenSearch)
    mocker.patch("opensearchpy.OpenSearch.__new__", return_value=mock_upstream)

    fake_client.index(fake_item)
