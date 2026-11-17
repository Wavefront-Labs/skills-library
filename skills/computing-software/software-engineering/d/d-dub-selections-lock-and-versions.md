---
id: computing-software.software-engineering.d.d-dub-selections-lock-and-versions
name: d-dub-selections-lock-and-versions
category: computing-software
field: software-engineering
product: d
tags: [d-dub-selections-lock-and-versions, dub-configuration, dub-selections-json, semver, version-range, dependency-pinning, dub-upgrade, git-dependency, path-dependency, lockfile, tilde-version, d]
level: practitioner
status: docs-checked
description: "Pin dependency versions with dub.selections.json, semver ranges (~> >= ==), path and git dependencies, dub upgrade, and committing the lock for apps versus libraries."
sources:
  - https://dub.pm/dub-reference/dependencies/
  - https://dub.pm/dub-reference/package_settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dub.selections.json, version ranges and lockfiles

Goal: reproducible dependency resolution.

- Range syntax: `"==1.2.3"` exact, `"~>1.2.3"` means >=1.2.3 <1.3.0, `"~>1.2"` means >=1.2.0 <2.0.0, `">=1.0.0 <2.0.0"`, `"*"` (any released version), `"~master"` branch (discouraged: use repository + version instead).
- `dub.selections.json` stores the selected versions; if a project has none, dub performs dependency resolution.
- Update: `dub upgrade` (latest allowed), `dub upgrade --prerelease`, `dub upgrade --missing-only`, `dub upgrade --verify`; show `dub list`, `dub describe`; `dub fetch pkg@x` (the `--version` option is deprecated).
- Other sources: `dependency "x" path="../x"`, `dependency "x" repository="git+https://host/repo.git" version="<commit>"`; `dub add-local <path> [<version>]` registers a local package directory (`dub add-path` registers a search path); `dub add-override` is deprecated.
- Optional deps: `optional=true` (only used if selected in `dub.selections.json`); `default=true` (needs `optional=true`) selects it when no selections file exists yet.
- Clean: `dub clean`, `dub clean-caches`, `dub remove pkg` removes a fetched package.

Gotchas:
- For public projects avoid `path` dependencies outside your package root, so users can build without managing external dependencies.

Verify: delete `dub.selections.json`, rebuild, and `git diff` to see drift.

## Checked

Date 2026-11-02. Confirmed version range syntax, optional and default dependency keys, repository dependencies and local packages (dub dependencies reference). Errors fixed: exact version is ==1.2.3; dub fetch --version and add-override are deprecated. Removed commit-the-selections advice.

Method: documentation only; no commands were run.
