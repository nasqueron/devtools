#!/usr/bin/env python3


import requests
import sys


#   -------------------------------------------------------------
#   GitHub API methods
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def query_api_repositories(github_account, page, repositories):
    url = f"https://api.github.com/orgs/{github_account}/repos?page={page}"

    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(
            f"HTTP error {response.status_code}: {response.text}")

    new_repositories = response.json()

    if len(new_repositories) == 0:
        # We've all of them.
        return repositories

    return query_api_repositories(
        github_account, page + 1, repositories + new_repositories)


def get_all_repositories(github_account):
    return query_api_repositories(github_account, 1, [])


def print_repository(repository_info, options):
    line = repository_info["name"]

    if options["with_branch"]:
        line += f",{repository_info['default_branch']}"

    print(line)


#   -------------------------------------------------------------
#   Application entry point
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def run(github_account, options):
    for repository in get_all_repositories(github_account):
        print_repository(repository, options)


if __name__ == "__main__":
    options = {
        "with_branch": False,
    }

    try:
        for extra_arg in sys.argv[2:]:
            if extra_arg == '-b':
                options["with_branch"] = True

        run(sys.argv[1], options)
    except IndexError:
        print("Usage:", sys.argv[0], "<GitHub org account>", file=sys.stderr)
        sys.exit(2)
