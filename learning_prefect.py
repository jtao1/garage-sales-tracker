import httpx
from prefect import flow, get_run_logger
from prefect.deployments import Deployment

@flow(retries=3, retry_delay_seconds=5)
def get_repo_info(repo_name: str = "PrefectHQ/prefect"):
    url = f"https://api.github.com/repos/{repo_name}"
    response = httpx.get(url)
    response.raise_for_status()
    repo = response.json()
    logger = get_run_logger()
    logger.info(f"PrefectHQ/prefect repository statistics 🤓:")
    logger.info(f"Stars 🌠 : {repo['stargazers_count']}")
    logger.info(f"Forks 🍴 : {repo['forks_count']}")


def deploy():
    deployment = Deployment.build_from_flow(
        flow=get_repo_info,
        name="prefect-example-deployment"
    )
    deployment.apply()

if __name__ == "__main__":
    deploy()
