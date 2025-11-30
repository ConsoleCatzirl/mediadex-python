from mediadex import mediainfo

import pytest
from pymediainfo import MediaInfo


def test_mediainfo_quick(mocker):
    expected = {"foo": "bar"}

    mock_parse = mocker.patch("pymediainfo.MediaInfo.parse", return_value=MediaInfo)
    mock_to_data = mocker.patch("pymediainfo.MediaInfo.to_data", side_effect=[expected, ])

    found = mediainfo.generate("mock/path")
    assert found == expected

    assert mock_parse.call_count == 1
    assert mock_to_data.call_count == 1


def test_mediainfo_retry(mocker):
    expected = {"foo": "bar"}
    encoding = {"encoding": "cp1252"}

    mock_parse = mocker.patch("pymediainfo.MediaInfo.parse", return_value=MediaInfo)
    mock_to_data = mocker.patch("pymediainfo.MediaInfo.to_data", side_effect=[FileNotFoundError, expected])
    mock_chardet = mocker.patch("chardet.detect", return_value=encoding)

    found = mediainfo.generate("mock/path")
    assert found == expected

    assert mock_parse.call_count == 2
    assert mock_to_data.call_count == 2
    assert mock_chardet.call_count == 1


def test_mediainfo_fail(mocker):
    encoding = {"encoding": "cp1252"}

    mock_parse = mocker.patch("pymediainfo.MediaInfo.parse", return_value=MediaInfo)
    mock_to_data = mocker.patch("pymediainfo.MediaInfo.to_data", side_effect=[FileNotFoundError, FileNotFoundError])
    mock_chardet = mocker.patch("chardet.detect", return_value=encoding)

    with pytest.raises(IOError):
        mediainfo.generate("mock/path")

    assert mock_parse.call_count == 2
    assert mock_to_data.call_count == 2
    assert mock_chardet.call_count == 1
