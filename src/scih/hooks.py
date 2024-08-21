from logging import info
from logging import warning
from os.path import exists
from subprocess import run
from typing import Annotated

from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException

from scih.app import app
from scih.app import get_sci_hooks
from scih.models.gitea import GiteaModel


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
        warning("did not receive the X-Gitea-Delivery request header - proceeding with being ambiguous")
        raise HTTPException(status_code=400)
    if x_gitea_event is None:
        warning("did not receive the X-Gitea-Event request header - proceeding with being ambiguous")
        raise HTTPException(status_code=400)
    info(f"got gitea event: {x_gitea_event}")
    if name not in sci_hooks:
        raise HTTPException(status_code=404, detail="no such hook found")
    if not exists(sci_hooks[name]):
        raise HTTPException(status_code=500, detail="could not find hook-file")
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
