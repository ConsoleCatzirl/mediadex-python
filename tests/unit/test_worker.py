from mediadex.worker import Worker


def test_worker_work(mocker, fake_config):
    mock_worker = Worker(fake_config)
    mock_worker.walk_path = mocker.MagicMock()

    mock_worker.work()
    # assert no exception is raised
