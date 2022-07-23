import code
import argparse
import importlib
import sys

import src

BANNER = """
                .    o8o  oooo   o8o      .    o8o                     
              .o8    `"'  `888   `"'    .o8    `"'                     
oooo  oooo  .o888oo oooo   888  oooo  .o888oo oooo   .ooooo.   .oooo.o 
`888  `888    888   `888   888  `888    888   `888  d88' `88b d88(  "8 
 888   888    888    888   888   888    888    888  888ooo888 `"Y88b.  
 888   888    888 .  888   888   888    888 .  888  888    .o o.  )88b 
 `V88V"V8P'   "888" o888o o888o o888o   "888" o888o `Y8bod8P' 8""888P' 
"""

def main():
    parser = argparse.ArgumentParser(
        description='Run a specific script by name. If no name is provided, start a REPL.'
    )
    parser.add_argument(
        'user_input',
        type=str,
        nargs='*',
        help='The name of the script that you want to run plus any arguments for that script.')
    parser.add_argument(
        '--version', action='store_true', help="Print out the version string."
    )

    args = parser.parse_args()
    user_input = args.user_input
    if args.version is True:
        print(src.__version__)
        sys.exit()
    if len(user_input) == 0:
        code.interact(banner=BANNER, local=locals())
    else:
        command_name = user_input.pop(0)
        module = importlib.import_module(f"src.commands.{command_name}")
        sys.exit(module.main(user_input))
