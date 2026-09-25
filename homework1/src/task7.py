"""Task 7: Package Management

Uses the third-party `requests` package (installed with pip) to fetch
public repository information from the GitHub API and summarize it.
"""
import requests

API_URL = "https://api.github.com/repos/{owner}/{repo}"


def fetch_repo_info(owner, repo, timeout=10):
    """Return the GitHub API's JSON data for a repository as a dict.

    Raises:
        ValueError: if owner or repo is empty.
        requests.HTTPError: if GitHub returns an error status (e.g. 404).
        requests.RequestException: for network problems such as timeouts.
    """
    if not owner or not repo:
        raise ValueError("owner and repo must both be non-empty")
    response = requests.get(
        API_URL.format(owner=owner, repo=repo),
        headers={"Accept": "application/vnd.github+json"},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def summarize_repo(info):
    """Return a one-line summary string from a repository info dict."""
    name = info.get("full_name", "unknown")
    stars = info.get("stargazers_count", 0)
    language = info.get("language") or "no language listed"
    return f"{name}: {stars} stars, written in {language}"


def main():
    """Fetch and print a summary of a real repository (needs internet)."""
    print(summarize_repo(fetch_repo_info("pytest-dev", "pytest")))


if __name__ == "__main__":
    main()
