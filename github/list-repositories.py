#!/usr/bin/env python3


import requests
import sys


#   -------------------------------------------------------------
#   GitHub API methods
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def query_api_repositories_for_names(github_account, page, repositories):
    url = f"https://api.github.com/orgs/{github_account}/repos?page={page}"

    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(
            f"HTTP error {response.status_code}: {response.text}")

    new_repositories = [repo["name"] for repo in response.json()]

    if len(new_repositories) == 0:
        # We've all of them.
        return repositories

    return query_api_repositories_for_names(
        github_account, page + 1, repositories + new_repositories)


def get_all_repositories_names(github_account):
    return query_api_repositories_for_names(github_account, 1, [])


#   -------------------------------------------------------------
#   Application entry point
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def run(github_account):
    for repository in get_all_repositories_names(github_account):
        print(repository)


if __name__ == "__main__":
    try:
        run(sys.argv[1])
    except IndexError:
        print("Usage:", sys.argv[0], "<GitHub org account>", file=sys.stderr)
        sys.exit(2)
