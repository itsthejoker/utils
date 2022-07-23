import httpx
import json
import sys
import zipfile
from datetime import datetime


def main(args):
    self_name = sys.argv[0].strip(".").strip("/")  # todo: is this resilient?
    data = json.loads(zipfile.ZipFile(self_name).read("environment.json"))
    build_time = datetime.fromisoformat(data['built_at'])

    release_data = httpx.get(
        'https://api.github.com/repos/itsthejoker/utils/releases/latest'
    )
    if release_data.status_code != 200:
        print(
            f"Something went wrong when talking to github; got a"
            f" {release_data.status_code} with the following content:\n"
            f"{release_data.content}"
        )
        sys.exit()
