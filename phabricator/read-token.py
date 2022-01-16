#!/usr/bin/env python3


import json
import os
import sys


#   -------------------------------------------------------------
#   Parse Phabricator configuration
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_phabricator_configuration_path():
    candidates = [
        os.environ["HOME"] + "/.arcrc",
        "/usr/local/etc/arcrc",
        "/etc/arcrc",
    ]

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    raise FileNotFoundError("Can't find Arc configuration")


def get_token(phabricator_url):
    config_path = get_phabricator_configuration_path()

    with open(config_path) as fd:
        config = json.load(fd)

    for instance, args in config.get("hosts", {}).items():
        if phabricator_url in instance:
            return args["token"]

    raise RuntimeError(
       f"{config_path} doesn't describe host {phabricator_url}")


#   -------------------------------------------------------------
#   Application entry point
#   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def run(phabricator_url):
    token = get_token(phabricator_url)
    print(token)


if __name__ == "__main__":
    try:
        phabricator_url_fragment = sys.argv[1]
    except IndexError:
        print("Usage:", sys.argv[0],
              "<Phabricator instance URL>", file=sys.stderr)
        sys.exit(2)

    run(phabricator_url_fragment)
