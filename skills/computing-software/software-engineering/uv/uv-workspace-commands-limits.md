---
id: computing-software.software-engineering.uv.uv-workspace-commands-limits
name: uv-workspace-commands-limits
category: computing-software
field: software-engineering
product: uv
tags: [uv, workspaces, monorepo, package-flag, workspace-sources, member-sources, editable, python]
level: practitioner
status: docs-checked
description: "Run commands in a uv workspace member with --package and handle workspace-level tool.uv.sources, member overrides, cross-workspace paths and the stated limits."
sources: [https://docs.astral.sh/uv/concepts/projects/workspaces/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workspace commands and sources

Goal: target the right member and get sources to resolve as intended.

## Method

- `uv run` and `uv sync` act on the workspace root by default. With root `albatross`, `uv run` and `uv run --package albatross` are equivalent; `uv run --package bird-feeder` runs the command in that member from any workspace directory.
- Depend on a member with `bird-feeder = { workspace = true }` in `[tool.uv.sources]`, plus the name in `dependencies`. This takes the package from the workspace instead of PyPI. Dependencies between members are editable.
- Sources set in the workspace root apply to all members unless a member overrides them. For example, a root `tqdm = { git = "https://github.com/tqdm/tqdm" }` makes every member install tqdm from GitHub.
- A member that defines `tool.uv.sources` for a dependency ignores the root's source for that dependency entirely, even if the member's source has a marker that does not match the current platform.
- `workspace` can be a path string to take a dependency from a different workspace. The path is resolved relative to the declaring project (or the workspace root for a workspace-level source), must point at the external workspace root, and uv selects the member matching the dependency name.

## Gotchas

- `uv run --package` does not exist for projects joined only by path dependencies; run from the package directory.
- A single `requires-python` applies to the workspace (the intersection of members).
- Python gives no dependency isolation, so uv cannot prevent a member importing another member's dependencies.

## Verify

In the page's example, `uv run` and `uv run --package albatross` behave identically, while `uv run --package bird-feeder` runs in the member.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/projects/workspaces). Removed or changed: removed an unfinished note about an --all-packages flag the page does not describe.

Method: documentation only; no commands were run.
