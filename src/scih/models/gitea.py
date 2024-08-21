from pydantic import BaseModel


class GiteaRepositoryModel(BaseModel):
    id: int
    name: str
    full_name: str
    description: str
    private: bool
    fork: bool
    html_url: str
    ssh_url: str
    clone_url: str
    default_branch: str
    created_at: str
    updated_at: str


class GiteaUserModel(BaseModel):
    name: str
    email: str
    username: str


class GiteaCommitModel(BaseModel):
    id: str
    message: str
    url: str
    author: GiteaUserModel
    committer: GiteaUserModel
    timestamp: str


class GiteaModel(BaseModel):
    secret: str
    ref: str
    before: str
    after: str
    compare_url: str
    commits: list[GiteaCommitModel]
    repository: GiteaRepositoryModel
