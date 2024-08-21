from subprocess import run

import pytest
from fastapi.testclient import TestClient

from scih.app import app
from scih.app import get_sci_hooks
from scih.hooks import *


@pytest.fixture()
def api(sci_conf: dict[str, str]) -> TestClient:
    app.dependency_overrides[get_sci_hooks] = lambda: sci_conf
    return TestClient(app)


@pytest.fixture()
def sci_conf() -> dict[str, str]:
    _ = run("touch /tmp/on-test", check=True, shell=True)
    return {"on-test": "/tmp/on-test"}


@pytest.fixture()
def gitea_example_body() -> str:
    return """{
            "secret": "3gEsCfjlV2ugRwgpU#w1*WaW*wa4NXgGmpCfkbG3",
            "ref": "refs/heads/develop",
            "before": "28e1879d029cb852e4844d9c718537df08844e03",
            "after": "bffeb74224043ba2feb48d137756c8a9331c449a",
            "compare_url": "http://localhost:3000/gitea/webhooks/compare/28e1879d029cb852e4844d9c718537df08844e03...bffeb74224043ba2feb48d137756c8a9331c449a",
            "commits": [
                {
                    "id": "bffeb74224043ba2feb48d137756c8a9331c449a",
                    "message": "Webhooks Yay!",
                    "url": "http://localhost:3000/gitea/webhooks/commit/bffeb74224043ba2feb48d137756c8a9331c449a",
                    "author": {
                        "name": "Gitea",
                        "email": "someone@gitea.io",
                        "username": "gitea"
                        },
                    "committer": {
                        "name": "Gitea",
                        "email": "someone@gitea.io",
                        "username": "gitea"
                        },
                    "timestamp": "2017-03-13T13:52:11-04:00"
                    }
                ],
            "repository": {
                "id": 140,
                "owner": {
                    "id": 1,
                    "login": "gitea",
                    "full_name": "Gitea",
                    "email": "someone@gitea.io",
                    "avatar_url": "https://localhost:3000/avatars/1",
                    "username": "gitea"
                    },
                "name": "webhooks",
                "full_name": "gitea/webhooks",
                "description": "",
                "private": false,
                "fork": false,
                "html_url": "http://localhost:3000/gitea/webhooks",
                "ssh_url": "ssh://gitea@localhost:2222/gitea/webhooks.git",
                "clone_url": "http://localhost:3000/gitea/webhooks.git",
                "website": "",
                "stars_count": 0,
                "forks_count": 1,
                "watchers_count": 1,
                "open_issues_count": 7,
                "default_branch": "master",
                "created_at": "2017-02-26T04:29:06-05:00",
                "updated_at": "2017-03-13T13:51:58-04:00"
           },
           "pusher": {
                  "id": 1,
                  "login": "gitea",
                  "full_name": "Gitea",
                  "email": "someone@gitea.io",
                  "avatar_url": "https://localhost:3000/avatars/1",
                  "username": "gitea"
          },
           "sender": {
                  "id": 1,
                  "login": "gitea",
                  "full_name": "Gitea",
                  "email": "someone@gitea.io",
                  "avatar_url": "https://localhost:3000/avatars/1",
                  "username": "gitea"
                  }
           }"""


@pytest.fixture()
def gitea_example_headers() -> dict[str, str]:
    return {
        "X-Gitea-Delivery": "test",  # normally a uuid
        "X-Gitea-Event": "test",
    }
