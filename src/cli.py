import code
import random
import string
import sys
import uuid

import click
import httpx
from shiv.bootstrap import current_zipfile

import src
from src.helpers import flip_char
from src.art import BANNERS


@click.group(
    context_settings=dict(help_option_names=["-h", "--help", "--halp"]),
    invoke_without_command=True,
)
@click.pass_context
@click.version_option(version=src.__version__, prog_name="utils")
def main(ctx):
    """Launch a utility or drop into a command line REPL if no command is given."""
    if ctx.invoked_subcommand is None:
        banner = random.choice(BANNERS)
        code.interact(banner=banner, local=globals())
        sys.exit()


@main.command()
def uuid4():
    """Generate a random UUID4."""
    click.echo(uuid.uuid4())


@main.command()
def ping():
    """Pong!"""
    click.echo("Pong!")


@main.command()
@click.argument("words", nargs=-1)
def beautify(words: list[str]):
    """
    MAkE YoUr mEsSaGe bEaUtIfUl!!!1!!

    WORDS is either a single string surrounded by double quotes or multiple bare words,
    e.g. `utils beautify "one two three"` or `utils beautify one two three`.
    """
    message = " ".join(words)
    new_beautiful_string = []

    for num, letter in enumerate(message):
        if letter in string.ascii_letters:
            if num % 2:
                new_beautiful_string.append(flip_char(letter))
                continue
        new_beautiful_string.append(letter)

    click.echo("".join(new_beautiful_string))


@main.command()
def update():
    """Get the newest release from GitHub and install it."""
    response = httpx.get(
        "https://api.github.com/repos/itsthejoker/utils/releases/latest"
    )
    if response.status_code != 200:
        print(
            f"Something went wrong when talking to github; got a"
            f" {response.status_code} with the following content:\n"
            f"{response.content}"
        )
        return
    release_data = response.json()
    if release_data["name"] == src.__version__:
        print("Server version is the same as current version; nothing to update.")
        return

    url = release_data["assets"][0]["browser_download_url"]
    with current_zipfile() as archive:
        with open(archive.filename, "wb") as f, httpx.stream("GET", url, follow_redirects=True) as r:
            for line in r.iter_bytes():
                f.write(line)
    print(f"Updated to {release_data['name']}! 🎉")


if __name__ == "__main__":
    main()
