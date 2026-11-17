---
id: computing-software.software-engineering.uv.uv-run-project-commands
name: uv-run-project-commands
category: computing-software
field: software-engineering
product: uv
tags: [uv, uv-run, project-environment, with, auto-sync, scripts, venv, python]
level: practitioner
status: docs-checked
description: "Run commands in the uv project environment with uv run, add per-invocation dependencies with --with, and control locking and syncing with flags."
sources: [https://docs.astral.sh/uv/concepts/projects/run/, https://docs.astral.sh/uv/concepts/projects/sync/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running commands with uv run

Goal: run code against the project's `.venv` without activating it.

## Method

- The project lives in `.venv`, isolated from the current shell, so `python -c "import example"` fails there. Use `uv run python -c "import example"`.
- `uv run` first makes sure the project environment is up to date (lock and sync). The command may come from the environment (`uv run example-cli foo`) or outside it (`uv run bash scripts/foo.sh`).
- Extra or different dependencies for one invocation: `uv run --with httpx==0.26.0 python -c "import httpx; print(httpx.__version__)"` prints `0.26.0`. The requested version wins even if the project requires another.
- Scripts with inline metadata (`# /// script` block) run isolated from the project with only their declared dependencies.

## Controlling auto-sync

- `uv run --locked`: error if `uv.lock` is out of date instead of updating it.
- `uv run --frozen`: use the lockfile without checking it is current.
- `uv run --no-sync`: do not check the environment is current.
- `uv run --exact`: exact syncing (remove extraneous packages); `uv run` is inexact by default.
- `--upgrade` / `--upgrade-package <name>` update lockfile and environment together.

## Gotchas

- Windows legacy setuptools scripts in `.venv\Scripts` are supported for `.ps1`, `.cmd`, `.bat`; the extension may be omitted and uv tries them in that order: `uv run --with nuitka==2.6.7 -- nuitka --version`.
- uv does not hand off the process; it forwards signals. On Unix most are forwarded except SIGKILL, SIGCHLD, SIGIO, SIGPOLL; SIGINT is forwarded only if sent more than once or the child's process group differs. On Windows uv ignores Ctrl-C and lets the child handle it.

## Verify

The `--with` example above prints `0.26.0`, and with `httpx==0.25.0` prints `0.25.0`.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/projects/run; concepts/projects/sync). Removed or changed: removed a bullet claiming the sync group and extra flags apply to uv run (the cited pages do not state it).

Method: documentation only; no commands were run.
