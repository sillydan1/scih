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
from argparse import ArgumentParser, Namespace

import uvicorn

from scih.app import app


def main() -> None:
    """Main entrypoint."""
    args = parse_arguments()
    # TODO: inject dependencies (using app.dependency_overrides[func_name])
    uvicorn.run(app, host=args.host, port=args.port)


def parse_arguments() -> Namespace:
    """Parse the commandline arguments.

    Returns:
        The parsed arguments as a Namespace.

    """
    parser = ArgumentParser(description="Simple CI webhooks api service")
    _ = parser.add_argument("--port", type=int, default=8000, help="Port to run the server on.")
    _ = parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on.")
    _ = parser.add_argument("--sci-conf-file", "-C", type=str, default="/etc/", help="dhjkwahdjkwah")  # BOOKMARK: here
    return parser.parse_args()
