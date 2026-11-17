---
id: computing-software.software-engineering.uv.uv-resolution-strategy
name: uv-resolution-strategy
category: computing-software
field: software-engineering
product: uv
tags: [uv, resolution, resolution-strategy, prerelease, fork-strategy, lower-bounds, lowest-direct]
level: practitioner
status: docs-checked
description: "Control which versions uv picks: highest or lowest, preferences from existing locks, pre-release modes, fork strategy, and why lower bounds matter."
sources: [https://docs.astral.sh/uv/concepts/resolution/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv resolution strategy

Goal: pick the versions uv resolves to, and test that declared lower bounds are real.

## Method

- Default: the latest version of each package. `flask>=2.0.0` yields the newest Flask, so tests never exercise the stated lower bound.
- `--resolution lowest`: lowest version of all direct and transitive dependencies. `--resolution lowest-direct`: lowest for direct dependencies, latest for the rest. Build dependencies always use the latest.
- Libraries: run tests in CI with `--resolution lowest` or `lowest-direct` to validate declared bounds.
- Preferences: an existing `uv.lock` or requirements output file, or an already installed version, is preferred. Versions change only if incompatible or you pass `--upgrade`.
- Pre-releases (`--prerelease`): default `if-necessary` prefers stable and falls back to pre-releases only if every stable candidate is rejected; `allow` considers them for all packages; `disallow` excludes them; `explicit` allows pre-releases only for first-party requirements that name a pre-release identifier.
- Per package: `--prerelease-package foo=allow`, or

```toml
[tool.uv]
prerelease = "disallow"
prerelease-package = { foo = "allow", bar = "if-necessary" }
```

- Multi-version (universal) resolution: `--fork-strategy requires-python` (default) picks the latest version per supported Python while minimizing distinct versions. For numpy with `>=3.8` it gives `numpy==1.24.4 ; python_version == "3.8"`, `numpy==2.0.2 ; python_version == "3.9"`, `numpy==2.2.0 ; python_version >= "3.10"`. `--fork-strategy fewest` minimizes versions instead, so numpy 1.24.4 for all.
- Lower bounds: `uv add` adds them by default and uv warns about direct dependencies without one. Without bounds the resolver can backtrack to the oldest version, which is slow, may fail to build, or may skip the conflicting dependency yet not work with your code.

## Verify

`uv pip compile --resolution lowest requirements.in -o requirements.txt` with `flask>=2.0.0` pins `flask==2.0.0` (docs example) instead of 3.0.0.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (concepts/resolution). Removed or changed: nothing needed removing.

Method: documentation only; no commands were run.
