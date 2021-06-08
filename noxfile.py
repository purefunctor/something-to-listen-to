import os
import tempfile

import nox


def install_with_constraints(session, *args, **kwargs):
    """
    https://cjolowicz.github.io/posts/hypermodern-python-03-linting/
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run_always(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            "--without-hashes",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(name="pre-commit")
def pre_commit(session):
    env = {"SKIP": "flake8"}

    install_with_constraints(session, "pre-commit")
    session.run("pre-commit", "install")
    session.run("pre-commit", "run", "--all-files", env=env)


@nox.session
def flake8(session):
    install_with_constraints(
        session,
        "flake8",
        "flake8-annotations",
        "flake8-docstrings",
        "flake8-import-order",
    )

    if os.getenv("GITHUB_ACTIONS"):
        session.run(
            "flake8",
            "--format=::error file=%(path)s,line=%(row)d,col=%(col)d::[flake8] %(code)s: %(text)s",
        )
    else:
        session.run("flake8")


@nox.session
def test(session):
    install_with_constraints(session, "pytest", "coverage[toml]")
    session.install(".")
    session.run("coverage", "run", "--branch", "-m", "pytest", "-vs")
    session.run("coverage", "report", "-m")
