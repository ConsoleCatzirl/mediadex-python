import json

import pytest

from mediadex.config import Config
from mediadex.app.worker import Worker


def test_worker_work(mocker):
    mock_worker = Worker(Config.defaults)
    mock_worker.work = mocker.MagicMock()

    mock_worker.work()
    # assert no exception is raised
