---
id: computing-software.cloud-infrastructure-engineering.saltstack.gitfs-per-remote-settings
name: gitfs-per-remote-settings
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, gitfs, mountpoint, root, base, per-remote, per-saltenv, refspecs]
level: advanced
status: docs-checked
description: "Override Salt GitFS options per remote and per saltenv (root, mountpoint, base, ref_types, all_saltenvs), the precedence order, and custom refspecs."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/tutorials/gitfs.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitFS per-remote and per-saltenv settings

Most global `gitfs_*` options can be overridden per remote using the same name without the `gitfs_` prefix (since 2014.7.0). The URL of a remote with per-remote options must end with a colon. `name` (needed to tell apart two entries for one repo), `saltenv` and `all_saltenvs` exist only per remote.

- `root`: serve only a subdirectory.
- `mountpoint`: prefix served paths.
- `base`: base branch.
- `ref_types`: restrict to branches or tags.
- `all_saltenvs` (2018.3.0) or `fallback` (3001): make one branch or tag appear in every saltenv. `all_saltenvs` overrides the branch-to-saltenv mapping and works only within GitFS; `fallback` also lets working branches be tested.
- Per-saltenv settings can override mountpoint, root and ref for individual environments.

Precedence, highest first: per-saltenv remote settings, global per-saltenv settings, per-remote settings, global settings.

Custom refspecs (2017.7.0): `gitfs_refspecs` fetches extra refs such as GitHub pull request refs; destinations must be under `refs/remotes/origin/`, and the path below that becomes the saltenv name (for example `pr/12345`). Refspecs can also be set per remote.

## Checked

2026-11-09. Read in full the Salt Git Fileserver Backend Walkthrough (doc/topics/tutorials/gitfs.rst, master branch): Per-remote and Per-Saltenv Configuration, Custom Refspecs, Global Remotes, Configuration Order of Precedence, root and mountpoint sections. Added the colon rule and version gates.

Method: documentation only; no commands were run.
