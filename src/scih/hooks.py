from os.path import exists
from subprocess import run
from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException

from scih.app import app
from scih.app import get_sci_hooks


@app.post("/hooks/gitea/{name}", description="post a gitea flavored hook")
def gitea(name: str, sci_hooks: Annotated[dict[str, str], Depends(get_sci_hooks)]):
    # TODO: Authentication (using secrets?)
    if name not in sci_hooks:
        raise HTTPException(status_code=404, detail="no such hook found")
    if not exists(sci_hooks[name]):
        raise HTTPException(status_code=500, detail="could not find hook-file")
    # TODO: Authorization (using ssh keys or something?)
    _ = run(f"touch {sci_hooks[name]}", check=True, shell=True)


@app.post("/hooks/github/{name}", description="post a github flavored hook")
def github(name: str, sci_hooks: Annotated[dict[str, str], Depends(get_sci_hooks)]):
    pass


@app.post("/hooks/generic/{name}", description="post a generic hook. May require some more configuration")
def generic(name: str, sci_hooks: Annotated[dict[str, str], Depends(get_sci_hooks)]):
    pass
