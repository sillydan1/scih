"""Hooks endpoint definitions.

This module should be *-imported by the main file to register all endpoints.
"""

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
from os.path import exists
from subprocess import run
from typing import Annotated

from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from loguru import logger

from scih.app import app
from scih.app import get_sci_hooks
from scih.model.gitea import GiteaModel


@app.post("/hooks/gitea/{name}", description="post a gitea flavored hook")
async def gitea(
    name: str,
    body: GiteaModel,
    sci_hooks: Annotated[dict[str, str], Depends(get_sci_hooks)],
    x_gitea_delivery: Annotated[str | None, Header()] = None,
    x_gitea_event: Annotated[str | None, Header()] = None,
) -> None:
    # TODO: Authentication (using secrets?)
    if x_gitea_delivery is None:
        logger.opt(colors=True).warning("did not receive the <red>X-Gitea-Delivery</red> request header")
        raise HTTPException(status_code=400)
    if x_gitea_event is None:
        logger.opt(colors=True).warning("did not receive the <red>X-Gitea-Event</red> request header")
        raise HTTPException(status_code=400)
    if name not in sci_hooks:
        logger.opt(colors=True).warning(f"no such hook found <light-blue>{name}</light-blue>")
        raise HTTPException(status_code=404, detail="no such hook found")
    if not exists(sci_hooks[name]):
        logger.opt(colors=True).error(f"could not find hook-file for: <light-blue>{name}</light-blue>")
        raise HTTPException(status_code=500, detail="could not find hook-file")
    logger.opt(colors=True).info(
        f"gitea: <yellow>{x_gitea_event}</yellow>, hook: <light-blue>{name}</light-blue>, repo: <green>{body.repository.name}</green>"
    )
    # TODO: Authorization (using ssh keys or something?)
    _ = run(f"touch {sci_hooks[name]}", check=True, shell=True)


# @app.post("/hooks/github/{name}", description="post a github flavored hook")
# async def github(name: str, sci_hooks: Annotated[dict[str, str], Depends(get_sci_hooks)]):
#     pass
#
#
# @app.post("/hooks/generic/{name}", description="post a generic hook. May require some more configuration")
# async def generic(name: str, sci_hooks: Annotated[dict[str, str], Depends(get_sci_hooks)]):
#     pass
