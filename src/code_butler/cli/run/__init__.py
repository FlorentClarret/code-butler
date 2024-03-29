import re
import tempfile
import time
from pathlib import Path
from typing import Iterable

import click
import git
from github import Github, Auth

from code_butler.cli import Application


@click.command(short_help="Analyze a repo then fix and open a PR if needed.")
@click.pass_obj
@click.argument("repos", nargs=-1)
def run(
    app: Application,
    repos: Iterable[str],
):
    client = Github(auth=Auth.Token(app.config_file.config.github.token))

    with tempfile.TemporaryDirectory() as temp_dir:
        for repo in repos:
            org_name, repo_name = repo.split("/")

            print(f"Repo: {org_name}/{repo_name}")
            repository = git.Repo.clone_from(
                f"git@github.com:{org_name}/{repo_name}.git",
                Path(temp_dir) / org_name / repo_name,
                depth=1,
            )
            upstream_repo = client.get_repo(f"{org_name}/{repo_name}")
            print(f"Cloned repo in: {repository.working_dir}")

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
                    print(f"{pattern} - File: {str(file)}")
                    path = Path(repository.working_dir) / str(file)
                    content = path.read_text()
                    found = True
                    content = re.sub(pattern, replace, content)
                    print("Updated file...")
                    path.write_text(content)
                    repository.index.add([str(file)])

            if found:
                print("Committing...")
                repository.index.commit(
                    "chore(ci): replace deprecated save-state and set-output commands"
                )
                print("Creating fork...")
                fork = upstream_repo.create_fork()
                print(f"Adding fork as remote... {fork.clone_url}")
                repository.create_remote("fork", fork.clone_url)
                # wait for GH to fork it properly
                time.sleep(2)
                print("Pushing...")
                repository.remotes.fork.push()

                print("Creating the PR...")
                pullrequest = upstream_repo.create_pull(
                    base="main",
                    head=f"{client.get_user().login}:main",
                    draft=True,
                    title="chore(ci): replace deprecated save-state and set-output commands",
                    body="See https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/",
                )
                print(f"PR: {pullrequest.html_url}")

    client.close()
