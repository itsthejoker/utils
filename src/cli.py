import code
import random
import string
import sys
import uuid

import click
import httpx
from rich import pretty
from rich import print as rprint
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
        def print_wrapper(*args, **kwargs):
            # I know this is dumb.
            # https://github.com/Textualize/rich/discussions/2462
            if "crop" in kwargs:
                del kwargs["crop"]
            rprint(*args, **kwargs)

        banner = random.choice(BANNERS)

        # source of code.interact, just expanded to fit Rich in there
        console = code.InteractiveConsole(globals())
        console.print = print_wrapper
        pretty.install(console)  # type: ignore
        try:
            import readline
        except ImportError:
            pass
        console.interact(banner, None)
        sys.exit()


@main.command()
def uuid4():
    """Generate a random UUID4."""
    click.echo(uuid.uuid4())


@main.command()
@click.argument("dice")
def roll(dice: str):
    """Roll some dice. Format: utils roll 3d8"""
    if "d" not in dice:
        click.echo("Missing part of the call. Example: 1d10")
        return
    if len(dice.split("d")) != 2:
        click.echo("Error parsing dice. Example: 2d6")
        return
    num, sides = dice.split("d")
    try:
        num = int(num)
        sides = int(sides)
    except ValueError:
        click.echo("Need numbers for the dice. Example: 30d4")
        return
    if num < 1 or sides < 1:
        click.echo("Dude. Example: 2d8")
        return
    values: list[int] = []
    for die in range(num):
        values.append(random.randint(1, sides))

    if num == 1:
        click.echo(f"You rolled a {values[0]}.")
    else:
        click.echo(f"You rolled: {'+'.join([str(item) for item in values])}")
        click.echo(f"Total: {sum(values)}")


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
                letter = flip_char(letter)
            new_beautiful_string.append(letter)

    click.echo("".join(new_beautiful_string))


@main.command()
def update():
    """Get the newest release from GitHub and install it."""
    response = httpx.get(
        "https://api.github.com/repos/itsthejoker/utils/releases/latest"
    )
    if response.status_code != 200:
        click.echo(
            f"Something went wrong when talking to GitHub; got a"
            f" {response.status_code} with the following content:\n"
            f"{response.content}"
        )
        return
    release_data = response.json()
    if release_data["name"] == src.__version__:
        click.echo("Server version is the same as current version; nothing to update.")
        return

    url = release_data["assets"][0]["browser_download_url"]
    with current_zipfile() as archive:
        with open(archive.filename, "wb") as f, httpx.stream("GET", url, follow_redirects=True) as r:
            for line in r.iter_bytes():
                f.write(line)
    click.echo(f"Updated to {release_data['name']}! 🎉")


if __name__ == "__main__":
    main()
