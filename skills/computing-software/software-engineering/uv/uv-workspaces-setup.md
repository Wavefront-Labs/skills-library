---
id: computing-software.software-engineering.uv.uv-workspaces-setup
name: uv-workspaces-setup
category: computing-software
field: software-engineering
product: uv
tags: [uv, workspaces, monorepo, workspace-members, shared-lockfile, tool-uv-workspace, python]
level: practitioner
status: docs-checked
description: "Create a uv workspace with tool.uv.workspace members and exclude globs, share one lockfile, and decide when workspaces or path dependencies fit better."
sources: [https://docs.astral.sh/uv/concepts/projects/workspaces/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Setting up a uv workspace

Goal: manage several interrelated packages in one repository with a single lockfile.

## Method

A workspace is a set of members managed together; each has its own `pyproject.toml`, but they share one `uv.lock`. Add a `tool.uv.workspace` table to a `pyproject.toml` to make that package the root (the root is also a member):

```toml
[project]
name = "albatross"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["bird-feeder", "tqdm>=4,<5"]

[tool.uv.sources]
bird-feeder = { workspace = true }

[tool.uv.workspace]
members = ["packages/*"]
exclude = ["packages/seeds"]
```

- `members` (required) and `exclude` (optional) are lists of globs. Every matched directory must contain a `pyproject.toml`. Members may be applications or libraries.
- `uv init` inside an existing package adds the new project to the workspace, creating the `tool.uv.workspace` table in the root if needed.
- In the layout above the members are `albatross` and `bird-feeder`; `seeds` is excluded.
- `uv lock` covers the whole workspace; `uv run` and `uv sync` default to the root.

## When to use

Use for interconnected packages in one repo: core library plus CLI tested separately, a library with a Rust/C++ extension module, or a library with plugins depending on the root.

Do not use when members have conflicting requirements or need separate virtual environments. Instead make each an independent project with path dependencies, e.g. `bird-feeder = { path = "packages/bird-feeder" }`; then `uv run --package` is unavailable and you run from the package directory.

## Gotchas

- One `requires-python` for the whole workspace: the intersection of all members. To test a member on another Python version, use `uv pip` in a separate virtual environment.
- uv cannot stop a member importing dependencies declared by another member.

## Verify

After `uv lock`, a single `uv.lock` sits at the workspace root.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/projects/workspaces). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
