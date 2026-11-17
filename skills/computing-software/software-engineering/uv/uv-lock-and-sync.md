---
id: computing-software.software-engineering.uv.uv-lock-and-sync
name: uv-lock-and-sync
category: computing-software
field: software-engineering
product: uv
tags: [uv, uv-lock, uv-sync, frozen, locked, upgrade, lockfile, python]
level: practitioner
status: docs-checked
description: "Create and check uv.lock, sync the environment, upgrade locked versions, and use --locked, --frozen, --inexact and partial-install flags."
sources: [https://docs.astral.sh/uv/concepts/projects/sync/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Locking and syncing

Goal: keep `uv.lock` and the environment consistent and upgrade deliberately.

## Method

- Locking resolves dependencies into `uv.lock`; syncing installs a subset of the lockfile into the environment. Both happen automatically in `uv run` and `uv sync`, and in commands that read the lockfile such as `uv tree`.
- Explicit: `uv lock`, `uv sync` (useful so the editor sees correct versions).
- Check: `uv lock --check`, equal to `--locked` on other commands (error rather than update). `--frozen` uses the lockfile unchecked. `--no-sync` skips the environment check.
- Outdated means it no longer matches project metadata: a new dependency, or a constraint that excludes the locked version. Constraint changes that still include the locked version leave it current. New package releases never make it outdated.
- Upgrade: `uv lock --upgrade` (all); `uv lock --upgrade-package <package>` (one, newest allowed); `uv lock --upgrade-package <package>==<version>`. Upgrades stay within project constraints. Git dependencies on a branch keep the locked commit unless an upgrade flag is used. The flags also work on `uv sync` and `uv run`.
- `uv sync` installs the project and workspace members editable; opt out with `--no-editable`. Without a build system the project is not installed.
- Exact by default: `uv sync` removes unselected packages; `uv sync --inexact` keeps them.
- Extras: `uv sync --extra foo`, `--all-extras`. Groups: `dev` is synced by default; `--no-dev`, `--only-dev`, `--group`, `--only-group`, `--no-group`, `--all-groups`, `--no-default-groups`.
- Export: `uv export --format requirements.txt`, `pylock.toml`, or `cyclonedx1.5`.

## Partial installs (for Docker layer caching)

`--no-install-project`, `--no-install-workspace`, `--no-install-package <name>`. Dependencies of the target are still installed. Misuse can leave a broken environment.

## Gotchas

- Exclusions beat inclusions: `uv sync --no-group foo --group foo` does not install `foo`.
- Malware check on sync is preview: set `audit.malware-check = true` or `UV_MALWARE_CHECK=1`; a match against OSV terminates the sync. Alternative service: `audit.malware-check-url` or `UV_MALWARE_CHECK_URL`.

## Verify

`uv lock --check` reports an error rather than updating when `uv.lock` is out of date.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/projects/sync). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
