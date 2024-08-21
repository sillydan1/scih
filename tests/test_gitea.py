from json import loads
from subprocess import run

from fastapi.testclient import TestClient


def get_file_mtime_ms(file: str) -> float:
    res = run(f"stat -c '%.Y' {file}", check=True, shell=True, capture_output=True).stdout.decode()
    return float(res.replace(",", ".").strip())


def test_post_gitea_hook_accept(
    api: TestClient, gitea_example_body: str, gitea_example_headers: dict[str, str], sci_conf: dict[str, str]
) -> None:
    """Simple acceptance test, that all available configurations will accept the gitea example body json."""
    for key in sci_conf:
        before = get_file_mtime_ms(sci_conf[key])
        assert before > 0, "You've somehow time travelled. How's the housing market treating you?"
        response = api.post(f"/hooks/gitea/{key}", json=loads(gitea_example_body), headers=gitea_example_headers)
        assert response.status_code == 200, response.json()
        after = get_file_mtime_ms(sci_conf[key])
        assert after > before
