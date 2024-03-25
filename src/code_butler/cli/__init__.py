import re
import tempfile
import time
from pathlib import Path

import click
import git
from github import Auth, Github

from code_butler.__about__ import __version__


def repos():
    yield "0k1745", "test-github-deprecation"


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.option(
    "--token",
    "-t",
    envvar="GITHUB_ACCESS_TOKEN",
)
@click.version_option(version=__version__, prog_name="Code Butler")
def code_butler(token):
    client = Github(auth=Auth.Token(token))

    with tempfile.TemporaryDirectory() as temp_dir:
        for org_name, repo_name in repos():
            print(f"Repo: {org_name}/{repo_name}")
            repo = git.Repo.clone_from(
                f"git@github.com:{org_name}/{repo_name}.git",
                Path(temp_dir) / org_name / repo_name,
                depth=1,
            )
            upstream_repo = client.get_repo(f"{org_name}/{repo_name}")
            print(f"Cloned repo in: {repo.working_dir}")

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
                for file in repo.git.execute(
                    ["git", "grep", "-l", search]
                ).splitlines():
                    print(f"{pattern} - File: {file}")
                    content = (Path(repo.working_dir) / file).read_text()
                    found = True
                    content = re.sub(pattern, replace, content)
                    print("Updated file...")
                    (Path(repo.working_dir) / file).write_text(content)
                    repo.index.add([file])

            if found:
                print("Committing...")
                repo.index.commit(
                    "chore(ci): replace deprecated save-state and set-output commands"
                )
                print("Creating fork...")
                fork = client.get_user().create_fork(upstream_repo)
                print(f"Adding fork as remote... {fork.clone_url}")
                repo.create_remote("fork", fork.clone_url)
                # wait for GH to fork it properly
                time.sleep(2)
                print("Pushing...")
                repo.remotes.fork.push()

                print("Creating the PR...")
                pullrequest = upstream_repo.create_pull(
                    base="main",
                    head="{}:{}".format("FlorentClarret", "main"),
                    draft=True,
                    title="chore(ci): replace deprecated save-state and set-output commands",
                    body="See https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/",
                )
                print(f"PR: {pullrequest.html_url}")

    client.close()
