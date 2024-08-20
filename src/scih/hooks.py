from scih.app import app


@app.post("/hooks/gitea/{name}", description="post a gitea flavored hook")
def gitea(name: str):
    pass


@app.post("/hooks/github/{name}", description="post a github flavored hook")
def github(name: str):
    pass


@app.post("/hooks/generic/{name}", description="post a generic hook. May require some more configuration")
def generic(name: str):
    pass
