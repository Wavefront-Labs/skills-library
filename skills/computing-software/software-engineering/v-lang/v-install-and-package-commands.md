---
id: computing-software.software-engineering.v-lang.v-install-and-package-commands
name: v-install-and-package-commands
category: computing-software
field: software-engineering
product: v-lang
tags: [v-install-and-package-commands, v-cli-maintenance, v install, vpm, v update, v remove, v search, v outdated, v list, package manager, v-lang]
level: practitioner
status: docs-checked
description: "Manage VPM and git-hosted modules with v install, update, upgrade, remove, search, list and outdated, and lock revisions in v.mod.lock."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# v install, update, remove, search and outdated

Goal: control dependencies from the CLI.

- Commands: `install`, `remove`, `search`, `update`, `upgrade` (all outdated packages), `list`, `outdated`.
- `v install ui` installs from VPM (https://vpm.vlang.io/). `v install [--once] [--git|--hg] [url]` installs from git or mercurial, for example `v install --git https://github.com/vlang/markdown`. `--once` installs only if not already installed.
- `v remove ui`, `v update ui` or `v update` for all, `v list` shows installed packages, `v outdated` shows those needing updates.
- Packages install to `~/.vmodules`; `VMODULES` overrides that. `v install --local` installs into the project's own lookup root (beside its `v.mod`).
- Run with no package inside a folder holding a `v.mod` and `v install` resolves its dependencies and writes `v.mod.lock` (requested, resolved, revision, url). Commit the lock. A plain `v install pkg` is global and records nothing.
- `v install --locked` fails instead of resolving anew (CI check); `--frozen` uses the lock without writing it.
- Semver ranges such as `vsl@^0.1.47` are supported. `v update -p PACKAGE --precise REF` picks an exact ref; `v update --latest` widens direct requirements and rewrites `v.mod`. `v why PACKAGE` and `v mod graph` work offline.

Gotchas:
- The global `VMODULES` folder holds one checkout of each package shared by all projects; installing in another project that locks different revisions switches them. Use `--local` for per-project checkouts.
- Names are normalised on install (`-` to `_`, lowercase), so the import path can differ from the package name.

Verify: `v list` shows the module and an `import` of it compiles.

## Checked

2026-11-08. Read: "Package management" through "Locking dependency revisions" in doc/docs.md (vlang/v). Corrected the draft's "no lock file" gotcha (`v.mod.lock` exists). Removed unconfirmed claims: the `VPM` tag-pin recipe and `author.mod` collision note. docs.vlang.io and modules.vlang.io dropped from sources.
Method: documentation only; no commands were run.
