import tempfile
import time
from pathlib import Path
from typing import Iterable

import click
import git
from git import GitCommandError
from github import Github, Auth
from github.GithubObject import NotSet

from code_butler.rules import ALL_RULES


@click.command(short_help="Analyze a repo then fix and open a PR if needed.")
@click.pass_context
@click.argument("repos", nargs=-1)
def run(
    ctx: click.Context,
    repos: Iterable[str],
):
    app = ctx.obj
    if not app.config_file.config.github.token:
        app.abort("No GitHub token found.")

    client = Github(auth=Auth.Token(app.config_file.config.github.token))

    with tempfile.TemporaryDirectory() as temp_dir:
        for repo in repos:
            org_name, repo_name = repo.split("/")

            app.console.print(f"Repo: {org_name}/{repo_name}")
            repository = git.Repo.clone_from(
                f"git@github.com:{org_name}/{repo_name}.git",
                Path(temp_dir) / org_name / repo_name,
                depth=1,
            )
            default_branch = repository.active_branch
            upstream_repo = client.get_repo(f"{org_name}/{repo_name}")
            app.console.print(f"Cloned repo in: {repository.working_dir}")

            found = False
            fork = None

            for rule in [r(repository) for r in ALL_RULES]:
                default_branch.checkout()
                for file in rule.detect():
                    found = True
                    app.console.print(f"{rule.id} - File: {str(file)}")
                    rule.fix(file)
                    repository.index.add([str(file)])

                if found:
                    app.console.print("Creating branch...")
                    new_branch = repository.create_head(rule.id)
                    new_branch.checkout()

                    app.console.print("Committing...")
                    repository.index.commit(rule.commit_message())
                    app.console.print("Creating fork...")
                    fork_org = app.config_file.config.github.fork_org or NotSet

                    if not fork:
                        fork = __create_fork(app, upstream_repo, repository, fork_org)

                    app.console.print("Pushing...")
                    repository.remotes.fork.push(new_branch)

                    app.console.print("Creating the PR...")
                    pullrequest = upstream_repo.create_pull(
                        base=fork.default_branch,
                        head=f"{fork_org}:{repository.active_branch.name}",
                        draft=True,
                        title=rule.pr_title(),
                        body=rule.pr_body(),
                    )
                    app.console.print(f"PR: {pullrequest.html_url}")

    client.close()


def __create_fork(app, upstream_repo, repository, fork_org):
    fork = upstream_repo.create_fork(fork_org, default_branch_only=True)

    try:
        app.console.print(f"Adding fork as remote... {fork.clone_url}")
        repository.create_remote("fork", fork.clone_url)
    except GitCommandError:
        app.console.print("Remote already exists.")

    # wait for GH to fork it properly
    time.sleep(2)

    return fork
