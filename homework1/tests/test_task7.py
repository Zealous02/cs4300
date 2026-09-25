"""Task 7: Package Management

Pytest tests for the requests-based code. The network is mocked, so the
tests are fast and pass without an internet connection.
"""
import pytest
import requests

import task7


class FakeResponse:
    """A minimal stand-in for requests.Response."""

    def __init__(self, data=None, status_code=200):
        self._data = data or {}
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")

    def json(self):
        return self._data


@pytest.fixture
def fake_get(monkeypatch):
    """Replace requests.get and record how it was called."""
    calls = {}

    def install(response=None, error=None):
        def _get(url, **kwargs):
            calls["url"] = url
            calls["kwargs"] = kwargs
            if error:
                raise error
            return response

        monkeypatch.setattr(task7.requests, "get", _get)
        return calls

    return install


def test_fetch_repo_info_returns_json(fake_get):
    data = {"full_name": "pytest-dev/pytest", "stargazers_count": 10}
    calls = fake_get(FakeResponse(data))
    assert task7.fetch_repo_info("pytest-dev", "pytest") == data
    assert calls["url"] == "https://api.github.com/repos/pytest-dev/pytest"
    assert calls["kwargs"]["timeout"] == 10


def test_http_error_is_raised(fake_get):
    fake_get(FakeResponse(status_code=404))
    with pytest.raises(requests.HTTPError):
        task7.fetch_repo_info("nobody", "nothing")


@pytest.mark.parametrize(
    "error", [requests.Timeout("slow"), requests.ConnectionError("offline")]
)
def test_network_errors_propagate(fake_get, error):
    fake_get(error=error)
    with pytest.raises(requests.RequestException):
        task7.fetch_repo_info("a", "b")


@pytest.mark.parametrize("owner, repo", [("", "repo"), ("owner", ""), ("", "")])
def test_empty_arguments_raise_value_error(owner, repo):
    with pytest.raises(ValueError):
        task7.fetch_repo_info(owner, repo)


@pytest.mark.parametrize(
    "info, expected",
    [
        (
            {"full_name": "a/b", "stargazers_count": 5, "language": "Python"},
            "a/b: 5 stars, written in Python",
        ),
        (
            {"full_name": "a/b", "stargazers_count": 0, "language": None},
            "a/b: 0 stars, written in no language listed",
        ),
        ({}, "unknown: 0 stars, written in no language listed"),
    ],
)
def test_summarize_repo(info, expected):
    assert task7.summarize_repo(info) == expected


def test_main_prints_summary(fake_get, capsys):
    fake_get(
        FakeResponse(
            {"full_name": "pytest-dev/pytest", "stargazers_count": 1, "language": "Python"}
        )
    )
    task7.main()
    assert "pytest-dev/pytest: 1 stars" in capsys.readouterr().out
