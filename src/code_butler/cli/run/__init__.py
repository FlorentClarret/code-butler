import re
import tempfile
import time
from pathlib import Path
from typing import Iterable

import click
import git
from github import Github, Auth
from github.GithubObject import NotSet


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
            upstream_repo = client.get_repo(f"{org_name}/{repo_name}")
            app.console.print(f"Cloned repo in: {repository.working_dir}")

            found = False

            for search, pattern, replace in (
                (
                    "::save-state name=",
                    r"::save-state name=([^:]*)::(.*)",
                    r'\g<1>=\g<2> >> "$GITHUB_STATE"',
                ),
                (
                    "::set-output name=",
                    r"::set-output name=([^:]*)::(.*)",
                    r'\g<1>=\g<2> >> "$GITHUB_OUTPUT"',
                ),
            ):
                for file in repository.git.execute(
                    ["git", "grep", "-l", search]
                ).splitlines():  # type: ignore
                    app.console.print(f"{pattern} - File: {str(file)}")
                    path = Path(repository.working_dir) / str(file)
                    content = path.read_text()
                    found = True
                    content = re.sub(pattern, replace, content)
                    app.console.print("Updated file...")
                    path.write_text(content)
                    repository.index.add([str(file)])

            if found:
                app.console.print("Committing...")
                repository.index.commit(
                    "chore(ci): replace deprecated save-state and set-output commands"
                )
                app.console.print("Creating fork...")
                fork_org = app.config_file.config.github.fork_org or NotSet

                fork = upstream_repo.create_fork(fork_org)
                app.console.print(f"Adding fork as remote... {fork.clone_url}")
                repository.create_remote("fork", fork.clone_url)
                # wait for GH to fork it properly
                time.sleep(2)
                app.console.print("Pushing...")
                repository.remotes.fork.push()

                app.console.print("Creating the PR...")
                pullrequest = upstream_repo.create_pull(
                    base=repository.active_branch.name,
                    head=f"{fork_org}:{repository.active_branch.name}",
                    draft=True,
                    title="chore(ci): replace deprecated save-state and set-output commands",
                    body="See https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/",
                )
                app.console.print(f"PR: {pullrequest.html_url}")

    client.close()
