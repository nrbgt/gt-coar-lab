# Copyright (c) 2020 University System of Georgia and GTCOARLab Contributors
# Distributed under the terms of the BSD-3-Clause License
import subprocess

import yaml

from . import meta as M
from . import paths as P

PROJ = yaml.safe_load(P.PROJ.read_text())
LOCK = yaml.safe_load(P.LOCK.read_text())


def _(args, **kwargs):
    """ a little wrapper to handle Paths for windows, and echoing
    """
    str_args = [str(a) for a in args]

    print("\n{}\n".format(" ".join(str_args)))

    if "cwd" in kwargs:
        kwargs["cwd"] = str(kwargs["cwd"])

    return subprocess.check_call(str_args, **kwargs)


def project_channels():
    return PROJ["env_specs"][M.INSTALLER_ENV_SPEC]["channels"]


def channel_args(pre=None, post=None):
    all_channels = [*(pre or []), *project_channels(), *(post or [])]
    return sum([["-c", c] for c in all_channels], [])


def conda_index():
    return _(["conda", "index", P.CONDA_DIST])


def git_commit():
    return subprocess.check_output(["git", "rev-parse", "--verify", "HEAD"]).decode(
        "utf-8"
    )[:7]


# doit stuff
def make_prepare_task(env_spec):
    def task():
        return dict(
            file_dep=[P.LOCK],
            targets=[P.ENVS / env_spec / "conda-meta" / "history"],
            actions=[[P.AP, "prepare", "--env-spec", env_spec]],
        )

    task.__name__ = f"task_prep_{env_spec}"
    task.__doc__ = f"prepare {env_spec} environment"

    return {task.__name__: task}


def make_lint_task(target, files):
    def task():
        return dict(file_dep=files, actions=[[*P.APR, "lint", target]])

    task.__name__ = f"task_lint_{target}"
    task.__doc__ = f"lint/format files with {target}"

    return {task.__name__: task}


def make_build_task(target, file_dep, targets):
    def task():
        return dict(
            file_dep=file_dep, targets=targets, actions=[[*P.APR, "build", target]]
        )

    task.__name__ = f"task_build_{target}"
    task.__doc__ = f"build {target}"

    return {task.__name__: task}
