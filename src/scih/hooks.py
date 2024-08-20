from typing import Annotated

from fastapi import Depends

from scih.app import app
from scih.app import get_sci_hooks


@app.post("/hooks/gitea/{name}", description="post a gitea flavored hook")
def gitea(name: str, sci_hooks: Annotated[dict[str, str], Depends(get_sci_hooks)]):
    pass


@app.post("/hooks/github/{name}", description="post a github flavored hook")
def github(name: str, sci_hooks: Annotated[dict[str, str], Depends(get_sci_hooks)]):
    pass


@app.post("/hooks/generic/{name}", description="post a generic hook. May require some more configuration")
def generic(name: str, sci_hooks: Annotated[dict[str, str], Depends(get_sci_hooks)]):
    pass
