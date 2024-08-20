"""Primary app module."""

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
from importlib import metadata

from fastapi import FastAPI

app = FastAPI(
    title="SCI-Hooks",
    description="Simple CI webhooks api service",
    version=metadata.version("scih"),
    contact={
        "name": "Asger Gitz-Johansen",
        "url": "https://git.gtz.dk/agj/scih",
    },
    license_info={
        "name": "GPLv3",
        "url": "https://www.gnu.org/licenses/",
    },
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url=None,
)
