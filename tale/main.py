"""
Main startup class

'Tale' mud driver, mudlib and interactive fiction framework
Copyright by Irmen de Jong (irmen@razorvine.net)
"""
import argparse
import sys
import traceback
from typing import Sequence

from . import __version__
from .driver import Driver
from .tio import DEFAULT_SCREEN_DELAY
from .story import GameMode


def get_driver(game_mode: GameMode, restricted: bool=False) -> Driver:
    if game_mode == GameMode.IF:
        return Driver()
    elif game_mode == GameMode.MUD:
        from .driver_mud import MudDriver
        return MudDriver(restricted)
    raise ValueError("invalid game mode")


def run_from_cmdline(cmdline: Sequence[str]) -> None:
    parser = argparse.ArgumentParser(description="""
        Tale framework %s game driver. Use this to launch a game and specify some settings.
        Sometimes the game will provide its own startup script that invokes this automatically.
        If it doesn't, refer to the options to see how to launch it manually instead.
        """ % __version__)
    parser.add_argument('-g', '--game', type=str, help='path to the game directory', required=True)
    parser.add_argument('-d', '--delay', type=int, help='screen output delay for IF mode (milliseconds, 0=no delay)',
                        default=DEFAULT_SCREEN_DELAY)
    parser.add_argument('-m', '--mode', type=str, help='game mode, default=if', default="if", choices=["if", "mud"])
    parser.add_argument('-i', '--gui', help='gui interface', action='store_true')
    parser.add_argument('-w', '--web', help='web browser interface', action='store_true')
    parser.add_argument('-r', '--restricted', help='restricted mud mode; do not allow new players', action='store_true')
    parser.add_argument('-z', '--wizard', help='force wizard mode on if story character (for debug purposes)', action='store_true')
    args = parser.parse_args(cmdline)
    try:
        game_mode = GameMode(args.mode)
        get_driver(game_mode, args.restricted).start(**vars(args))
    except:
        if args.gui:
            tb = traceback.format_exc()
            from .tio import tkinter_io
            tkinter_io.show_error_dialog("Exception during start", "An error occurred while starting up the game:\n\n" + tb)
        raise


if __name__ == "__main__":
    run_from_cmdline(sys.argv[1:])
