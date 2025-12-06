import os

from mediadex import item


def test_item(mocker):
    mock_item = item.Item("mock", "mock", "mock", "mock")

    mocker.patch("os.lstat", return_value=mocker.MagicMock(spec=os.stat_result))

    mock_finger = mocker.patch("mediadex.fingerprint.generate", return_value="fingerprint")
    mock_minfo = mocker.patch("mediadex.mediainfo.generate", return_value="mediainfo")

    _ = mock_item.document
    _ = mock_item.document

    mock_finger.assert_called_once()
    mock_minfo.assert_called_once()
