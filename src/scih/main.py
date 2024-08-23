"""Main scih module."""

"""
 scih - Simple CI webhooks integration extension
   Copyright (C) 2024 Asger Gitz-Johansen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from argparse import ArgumentParser
from argparse import Namespace
from os import environ
from os.path import exists
from sys import stdout

import uvicorn
from loguru import logger

from scih.app import app
from scih.app import get_sci_hooks
from scih.config.cached_conf_reader import CachedConfReader
from scih.hooks import *


@logger.catch
def main() -> None:
    """Main entrypoint."""
    args = parse_arguments()
    if args is None:
        return
    use_colors: bool = not bool(environ.get("NO_COLOR", ""))
    setup_logging(args.verbosity, use_colors)
    conf_loader = CachedConfReader(args.sci_conf_file)
    app.dependency_overrides[get_sci_hooks] = lambda: conf_loader.config
    uvicorn.run(app, host=args.host, port=args.port, use_colors=use_colors)


def setup_logging(level: str, use_colors: bool) -> None:
    logger.remove()  # A fresh start
    _ = logger.add(
        stdout,
        colorize=use_colors,
        format="{time:HH:mm:ss} <level>{level}</level> <fg #888>{file}:{line}:</fg #888> {message}",
        level=level,
    )


def parse_arguments() -> Namespace | None:
    """Parse the commandline arguments.

    Returns:
        The parsed arguments as a Namespace.

    """
    parser = ArgumentParser(description="Simple CI webhooks api service")
    _ = parser.add_argument("--port", "-P", type=int, default=8000, help="Port to run the server on.")
    _ = parser.add_argument("--host", "-H", type=str, default="0.0.0.0", help="Host to run the server on.")
    _ = parser.add_argument(
        "--verbosity",
        "-v",
        type=str,
        default="SUCCESS",
        help="Set verbosity level.",
        choices=["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"],
    )
    _ = parser.add_argument(
        "--sci-conf-file", "-c", type=str, default="/etc/sci/pipelines.conf", help="Sci pipelines configuration file."
    )
    _ = parser.add_argument(
        "--sci-trigger-dir", "-t", type=str, default="/tmp/sci", help="Directory where sci triggers are."
    )
    args = parser.parse_args()
    if not exists(args.sci_conf_file):
        print(f"ERROR: no such file exists: {args.sci_conf_file}")
        parser.print_help()
        return None
    return args
