#!/usr/bin/env python3


import sys
import json


#   -------------------------------------------------------------
#   Application container
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

app = {
    "base_url": "https://<phabricator>",
    "issues": {},
}


#   -------------------------------------------------------------
#   Analyze Phabricator repositories metadata
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def analyze_repository(repository):
    id = repository["id"]
    settings_url = f"{app['base_url']}/diffusion/edit/{id}/page/basics/"
    call_sign = repository["fields"]["callsign"]
    short_name = repository["fields"]["shortName"]
    issues = []

    if repository["fields"]["defaultBranch"] == "master":
        issues.append(
            ("defaultBranch-master",
             "Has still a master branch. Rename it to main."))

    if not short_name:
        issues.append(
            ("shortName-missing",
             f"Short name is missing. Add one here: {settings_url}"))

    if not contains_github_url(repository):
        issues.append(
            ("github-missing", "Repository should be mirrored to GitHub"))
    else:
        if short_name:
            github_name = get_github_repository_name(repository)
            if short_name != github_name:
                issues.append(
                    ("github-invalidName",
                     f"Repository is called {short_name} on Phabricator but {github_name} on GitHub."))

        url_id, has_valid_io = check_github_io(repository)
        if not has_valid_io:
            url_url = f"{app['base_url']}/diffusion/{call_sign}/uri/edit/{url_id}/"
            issues.append(
                ("github-io-mirror",
                 f"GitHub URL isn't configured as a mirror. Edit here: {url_url}"))

    if issues:
        app["issues"][repository["fields"]["callsign"]] = issues


def analyze_repositories(repositories):
    guess_phabricator_config(repositories)

    for repository in repositories:
        analyze_repository(repository)

    print_issues()


def guess_phabricator_config(repositories):
    url = guess_phabricator_url(repositories[0])
    if url:
        app["base_url"] = url


def guess_phabricator_url(repository):
    for uri in repository["attachments"]["uris"]["uris"]:
        if "<base-uri>" in uri["fields"]["uri"]["normalized"]:
            url = uri["fields"]["uri"]["effective"]
            pos_start = url.find("://")
            pos_end = url.find("/diffusion/")
            return "https" + url[pos_start:pos_end]


def contains_github_url(repository):
    for uri in repository["attachments"]["uris"]["uris"]:
        if 'github.com/' in uri["fields"]["uri"]["normalized"]:
            return True


def get_github_repository_name(repository):
    for uri in repository["attachments"]["uris"]["uris"]:
        url = uri["fields"]["uri"]["normalized"]
        if 'github.com/' in url:
            # Normalized URL is github.com/<account>/<repo>, take last part
            return url.split("/")[-1]


def check_github_io(repository):
    for uri in repository["attachments"]["uris"]["uris"]:
        if 'github.com/' in uri["fields"]["uri"]["normalized"]:
            return uri["id"], uri["fields"]["io"]["effective"] == "mirror"


def print_issues():
    for repository, issues in app["issues"].items():
        print(f"r{repository}")
        for issue in issues:
            print(f"\t[{issue[0]}] {issue[1]}")
        print()


#   -------------------------------------------------------------
#   Application entry point
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def run(repositories_path):
    repositories = json.load(open(repositories_path))
    analyze_repositories(repositories["result"]["data"])


if __name__ == "__main__":
    try:
        repositories_path = sys.argv[1]
    except IndexError:
        print("Usage:", sys.argv[0],
              "<repositories API response file>", file=sys.stderr)
        sys.exit(2)

    run(repositories_path)
