import httpx

import src


def main(args):
    release_data = httpx.get(
        "https://api.github.com/repos/itsthejoker/utils/releases/latest"
    )
    if release_data.status_code != 200:
        print(
            f"Something went wrong when talking to github; got a"
            f" {release_data.status_code} with the following content:\n"
            f"{release_data.content}"
        )
        return
    json_data = release_data.json()
    if json_data["name"] == src.__version__:
        print("Server version is the same as current version; nothing to update.")
        return

    url = json_data["assets"][0]["browser_download_url"]
    with open("utils", "wb") as f, httpx.stream("GET", url, follow_redirects=True) as r:
        for line in r.iter_bytes():
            f.write(line)
    print(f"Updated to {json_data['name']}! 🎉")
