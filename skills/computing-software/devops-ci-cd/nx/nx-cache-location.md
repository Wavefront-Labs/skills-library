---
id: computing-software.devops-ci-cd.nx.nx-cache-location
name: nx-cache-location
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, caching, cachedirectory, nx-cache-directory, ci, sandbox]
level: practitioner
status: docs-checked
description: "Where Nx stores its local cache (shared per-user directory by id), how cacheDirectory and NX_* variables opt out, CI caching implications and fallback behaviour."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/kb/change-cache-location.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know and control where the local Nx cache lives.

Default: `~/.nx/<id>/cache` (plus `~/.nx/<id>/databases`), outside the workspace. The id identifies the workspace (its Nx Cloud id, otherwise a key derived from the git remote), not the folder. Main checkout, git worktrees and a second clone share one cache, so renaming/moving a checkout keeps it. A workspace with no derivable identity (e.g. not a git repo) keeps its own copy. Cache entries are kept for a week.

Change it in `nx.json`:

```json
{ "cacheDirectory": "/tmp/mycache" }
```

Opting out of the shared location: setting `cacheDirectory`, `NX_CACHE_DIRECTORY`, `NX_WORKSPACE_DATA_DIRECTORY` or `NX_PROJECT_GRAPH_CACHE_DIRECTORY` makes Nx use what you configured, in the checkout that configures it.

CI: Nx no longer writes to `.nx/cache` by default. Point the CI cache step at `~/.nx`, or set `NX_CACHE_DIRECTORY` to restore the old location.

AI agent sandboxes: `~/.nx` is spelled the same on every machine, so a sandbox grant can be committed; `nx configure-ai-agents` writes it into `.claude/settings.json` for Claude Code.

Fallback: if Nx cannot use `~/.nx`, the checkout keeps its own `.nx` directories. Causes: it cannot make the directory owner-only (typically `sudo nx` that kept your `HOME`, leaving root ownership), or the process cannot write there (a sandbox). Nx detects the latter by writing a marker file.

Cleanup: `nx reset` clears the shared directory for the current workspace and the checkout's own. Directories of workspaces no longer checked out anywhere are never reclaimed; delete them by hand.

## Checked

2026-11-07. Confirmed: the NX_CACHE_DIRECTORY / cacheDirectory behaviour and nx reset note against the Change cache location page. Removed: an invented Verify step.

Method: documentation only; no commands were run.
