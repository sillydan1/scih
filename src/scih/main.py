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

import uvicorn

from scih.app import app
from scih.app import get_sci_hooks
from scih.hooks import *


def main() -> None:
    """Main entrypoint."""
    args = parse_arguments()

    conf = read_config_file(args.sci_conf_file)
    def get_sci_hooks_from_conf(conf: dict[str, str] = conf) -> dict[str, str]:
        return conf

    app.dependency_overrides[get_sci_hooks] = get_sci_hooks_from_conf
    uvicorn.run(app, host=args.host, port=args.port)


def read_config_file(filepath: str) -> dict[str, str]:
    result: dict[str, str] = {}
    with open(filepath, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        pass  # TODO: interpret the line
    return result


def parse_arguments() -> Namespace:
    """Parse the commandline arguments.

    Returns:
        The parsed arguments as a Namespace.

    """
    parser = ArgumentParser(description="Simple CI webhooks api service")
    _ = parser.add_argument("--port", type=int, default=8000, help="Port to run the server on.")
    _ = parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on.")
    _ = parser.add_argument(
        "--sci-conf-file", "-C", type=str, default="/etc/sci/pipelines.conf", help="sci pipelines configuration file."
    )
    return parser.parse_args()
